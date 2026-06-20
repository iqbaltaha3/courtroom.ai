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
    "judge":          ("Judge",          "Agent 8"),
    "reporter":       ("Court Reporter", "Agent 9"),
    "consultant":     ("Internal Consultant", "Simulation Review"),
    "top_consultant": ("Consultant Sparrow", "Executive Advisory"),
}

# Map node name → which state key holds its output (used for the SSE
# "content" field — the flattened text version, for simple display)
NODE_OUTPUT_KEY = {
    "case_manager":   "entities",
    "legal_research": "laws",
    "consultant":     "consultant",
    "top_consultant": "top_consultant",
    "prosecutor_r1":  "pros_r1",
    "defense_r1":     "def_r1",
    "prosecutor_r2":  "pros_r2",
    "defense_r2":     "def_r2",
    "judge":          "verdict",
    "reporter":       "report",
}

# Map node name → which state key (if any) holds its structured Pydantic
# output, sent alongside "content" so frontends can render real fields
# instead of re-parsing flattened text.
NODE_STRUCTURED_KEY = {
    "case_manager":   "case_intake",
    "legal_research": "legal_research",
    "judge":          "judge_verdict",
}


def _empty_state(complaint: str) -> dict:
    return {
        "complaint": complaint,
        "entities": None, "accused": None, "offence": None, "victim": None,
        "facts": None, "case_intake": None,
        "laws": None, "sections_applied": None, "precedents": None,
        "legal_research": None,
        "consultant": None,
        "top_consultant": None,
        "pros_r1": None, "def_r1": None,
        "pros_r2": None, "def_r2": None,
        "verdict": None, "verdict_short": None,
        "confidence": None, "reasoning": None, "probable_punishment": None,
        "judge_verdict": None,
        "headline": None, "report": None,
    }


class SimulateRequest(BaseModel):
    complaint: str


@app.post("/simulate")
async def simulate(req: SimulateRequest):
    """Stream each agent's output as Server-Sent Events."""

    async def event_stream():
        initial_state = _empty_state(req.complaint)

        # stream_mode="updates" yields {node_name: partial_state} after each node
        for node_name, partial in court_graph.stream(
            initial_state, stream_mode="updates"
        ):
            label, role = NODE_LABELS.get(node_name, (node_name, ""))
            output_key  = NODE_OUTPUT_KEY.get(node_name, "")
            content     = partial.get(output_key, "")

            structured_key = NODE_STRUCTURED_KEY.get(node_name)
            structured = partial.get(structured_key) if structured_key else None

            payload = json.dumps({
                "node":       node_name,
                "label":      label,
                "role":       role,
                "content":    content,
                "structured": structured,   # dict or None
            })
            yield {"event": "agent", "data": payload}
            await asyncio.sleep(0)   # let the event loop breathe

        yield {"event": "done", "data": json.dumps({"status": "complete"})}

    return EventSourceResponse(event_stream())


@app.post("/simulate/full")
async def simulate_full(req: SimulateRequest):
    """Non-streaming: return complete final state as JSON."""
    initial_state = _empty_state(req.complaint)
    result = court_graph.invoke(initial_state)
    return result