# Courtroom AI — Full Blueprint

## Project structure

```
courtroom_ai/
├── agents/
│   ├── __init__.py
│   ├── case_manager.py       # Agent 1
│   ├── legal_research.py     # Agent 2
│   ├── prosecutor.py         # Agent 3
│   ├── defense.py            # Agent 4
│   ├── judge.py              # Agent 5
│   └── reporter.py           # Agent 6
├── graph/
│   ├── __init__.py
│   ├── state.py              # Shared TypedDict state
│   └── graph.py              # LangGraph wiring
├── api/
│   ├── __init__.py
│   └── main.py               # FastAPI server + SSE streaming
├── frontend/
│   └── src/
│       ├── App.jsx
│       └── CourtRoom.jsx
├── tests/
│   └── test_graph.py
├── .env.example
├── requirements.txt
└── BLUEPRINT.md
```

---

## Step-by-step build guide

### Step 0 — Prerequisites
```
Python 3.11+
Node 18+
Anthropic API key
```

### Step 1 — Install dependencies
```bash
pip install langgraph langchain-anthropic fastapi uvicorn python-dotenv sse-starlette
```

### Step 2 — Define shared state  →  graph/state.py
Single TypedDict that every agent reads from and writes to.
All agents receive the full state; each writes only its own field.

### Step 3 — Build each agent  →  agents/*.py
Each agent is one function:
  - Takes `state: CourtState`
  - Calls Claude with a role-specific system prompt
  - Returns `{"field_name": response_text}`

Order: case_manager → legal_research → prosecutor_r1 → defense_r1
       → prosecutor_r2 → defense_r2 → judge → reporter

### Step 4 — Wire the graph  →  graph/graph.py
```python
graph.add_node("case_manager", run_case_manager)
graph.add_node("legal_research", run_legal_research)
...
graph.add_edge("case_manager", "legal_research")
graph.add_edge("legal_research", "prosecutor_r1")
...
```
Sequential. No branching needed for MVP.

### Step 5 — FastAPI server  →  api/main.py
One POST endpoint `/simulate` that:
  1. Accepts `{"complaint": "..."}` 
  2. Streams each agent's output via SSE as it completes
  3. Returns final state JSON at the end

### Step 6 — Frontend  →  frontend/src/
React app that:
  1. POSTs the complaint
  2. Listens to the SSE stream
  3. Renders each agent card as it arrives

### Step 7 — Test
```bash
python tests/test_graph.py
```
Runs the full graph with a sample complaint, prints all outputs.

---

## Data flow

```
User complaint
     │
     ▼
CourtState (initialized)
     │
  [case_manager]    → writes: entities, accused, offence
     │
  [legal_research]  → writes: laws, sections, precedents
     │
  [prosecutor_r1]   → writes: pros_r1
     │
  [defense_r1]      → writes: def_r1
     │
  [prosecutor_r2]   → writes: pros_r2
     │
  [defense_r2]      → writes: def_r2
     │
  [judge]           → writes: verdict, confidence, sections_applied
     │
  [reporter]        → writes: report, headline
     │
     ▼
Final CourtState (complete)
```

---

## Environment variables

```
ANTHROPIC_API_KEY=sk-ant-...
MODEL=claude-sonnet-4-6
MAX_TOKENS=800
```
