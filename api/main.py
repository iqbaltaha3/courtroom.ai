import json
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from graph.graph import court_graph

app = FastAPI(title="Courtroom AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Map node name → display label for the frontend
NODE_LABELS = {
    "case_manager":   ("Case Manager",   "Agent 1"),
    "legal_research": ("Legal Research", "Agent 2"),
    "prosecutor_r1":  ("Prosecutor",     "Round 1"),
    "defense_r1":     ("Defense Counsel","Round 1"),
    "prosecutor_r2":  ("Prosecutor",     "Round 2"),
    "defense_r2":     ("Defense Counsel","Round 2"),
    "judge":          ("Judge",          "Agent 5"),
    "reporter":       ("Court Reporter", "Agent 6"),
}

# Map node name → which state key holds its output
NODE_OUTPUT_KEY = {
    "case_manager":   "entities",
    "legal_research": "laws",
    "prosecutor_r1":  "pros_r1",
    "defense_r1":     "def_r1",
    "prosecutor_r2":  "pros_r2",
    "defense_r2":     "def_r2",
    "judge":          "verdict",
    "reporter":       "report",
}


class SimulateRequest(BaseModel):
    complaint: str


@app.post("/simulate")
async def simulate(req: SimulateRequest):
    """Stream each agent's output as Server-Sent Events."""

    async def event_stream():
        initial_state = {
            "complaint": req.complaint,
            "entities": None, "accused": None, "offence": None,
            "laws": None,
            "pros_r1": None, "def_r1": None,
            "pros_r2": None, "def_r2": None,
            "verdict": None, "verdict_short": None,
            "confidence": None, "sections_applied": None,
            "headline": None, "report": None,
        }

        # stream_mode="updates" yields {node_name: partial_state} after each node
        for node_name, partial in court_graph.stream(
            initial_state, stream_mode="updates"
        ):
            label, role = NODE_LABELS.get(node_name, (node_name, ""))
            output_key  = NODE_OUTPUT_KEY.get(node_name, "")
            content     = partial.get(output_key, "")

            payload = json.dumps({
                "node":    node_name,
                "label":   label,
                "role":    role,
                "content": content,
            })
            yield {"event": "agent", "data": payload}
            await asyncio.sleep(0)   # let the event loop breathe

        yield {"event": "done", "data": json.dumps({"status": "complete"})}

    return EventSourceResponse(event_stream())


@app.post("/simulate/full")
async def simulate_full(req: SimulateRequest):
    """Non-streaming: return complete final state as JSON."""
    initial_state = {
        "complaint": req.complaint,
        "entities": None, "accused": None, "offence": None,
        "laws": None,
        "pros_r1": None, "def_r1": None,
        "pros_r2": None, "def_r2": None,
        "verdict": None, "verdict_short": None,
        "confidence": None, "sections_applied": None,
        "headline": None, "report": None,
    }
    result = court_graph.invoke(initial_state)
    return result
