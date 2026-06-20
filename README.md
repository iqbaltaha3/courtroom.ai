# Courtroom AI

Courtroom AI is a multi-agent legal simulation project that processes a complaint through a sequence of AI agents and produces a structured courtroom-style output.

## What it does

The application takes a user complaint and runs it through a graph of agents that:
- identify key entities and facts,
- research relevant laws and precedents,
- generate prosecution and defense arguments,
- produce a judge's verdict, and
- create a final report.

## Project structure

- `app.py` — Streamlit UI for running the simulation from a browser.
- `api/main.py` — FastAPI server with streaming endpoints.
- `agents/` — Individual agent implementations.
- `graph/` — LangGraph workflow and shared state schema.
- `tests/` — Sample test coverage for the graph.
- `requirements.txt` — Python dependencies.
- `BLUEPRINT.md` — Detailed implementation plan.

## Prerequisites

- Python 3.11+
- A valid API key for your configured LLM provider (the project expects environment configuration such as `ANTHROPIC_API_KEY`)

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables in a `.env` file (or your shell environment). At minimum, make sure the required model/API settings are present.

## Running the app

### Streamlit UI

```bash
python app.py
```

Then open the local URL shown by Streamlit.

### FastAPI server

```bash
uvicorn api.main:app --reload
```

The API exposes endpoints such as:
- `POST /simulate` for streaming updates
- `POST /simulate/full` for the complete final result

## Running tests

```bash
python -m pytest
```

## How the workflow works

The graph runs in this order:
1. `case_manager`
2. `legal_research`
3. `consultant`
4. `prosecutor_r1`
5. `defense_r1`
6. `prosecutor_r2`
7. `defense_r2`
8. `judge`
9. `reporter`

Each stage updates the shared state used by the next stage.

## Notes

- The codebase is designed around a LangGraph workflow.
- The current UI is a simple demo interface for entering a complaint and viewing simulation output.
- For production use, you should review prompts, validation, safety controls, and model configuration.
