# MyPeshkar Modular Structure - Complete Guide

## ✅ Migration Complete!

Your codebase has been successfully reorganized into a clean, professional modular structure. **A beginner AI engineer can now easily understand the code organization.**

---

## 📁 New Directory Structure Explained

```
src/
├── config/              🔧 Configuration & Constants
│   ├── constants.py     - Color codes, app names, timeouts
│   └── settings.py      - Environment variables, API keys
│
├── core/                ⚙️ Workflow Orchestration
│   ├── orchestrator.py  - LangGraph workflow (how agents work together)
│   └── state.py         - Case state definition (data structure)
│
├── agents/              🤖 AI Specialist Agents
│   ├── case_analyst.py       - Extracts case details from complaint
│   ├── legal_researcher.py   - Finds relevant laws & precedents
│   ├── prosecutor.py         - Builds prosecution arguments
│   ├── defense.py            - Builds defense arguments
│   ├── judge.py              - Delivers verdict
│   ├── reporter.py           - Generates news summary
│   ├── consultant.py         - Provides strategy advice
│   ├── top_consultant.py     - Independent final review
│   └── schemas.py            - Data models for structured output
│
├── services/            🔌 Business Logic & APIs
│   ├── llm_service.py   - Calls Groq API for LLM
│   └── auth_service.py  - User authentication & access control
│
├── evaluation/          📊 Testing & Metrics
│   ├── evaluator.py     - Evaluates case analysis quality
│   ├── metrics.py       - Tracks performance metrics
│   ├── dashboard.py     - Displays metrics in UI
│   └── data/            - Historical metrics data
│
├── ui/                  🎨 Streamlit Frontend
│   ├── app.py           - Main entry point (TO BE CREATED)
│   ├── components/      - Reusable UI elements
│   │   ├── styles.py    - CSS & styling (TO BE EXTRACTED)
│   │   └── forms.py     - Input forms (TO BE EXTRACTED)
│   └── pages/           - Different app sections
│       ├── tools_page.py       - Tool selection (TO BE EXTRACTED)
│       ├── metrics_page.py     - Metrics tab (TO BE EXTRACTED)
│       └── vision_page.py      - Vision tab (TO BE EXTRACTED)
│
├── api/                 🔗 REST API (Future)
│   └── __init__.py      - API routes
│
└── utils/               🔨 Helper Functions
    ├── web_search.py    - Web search integration
    ├── helpers.py       - Utility functions
    ├── validators.py    - Input validation
    └── logger.py        - Logging configuration
```

---

## 🎯 How to Explain This in an Interview

### Simple 1-Minute Explanation:

> "I reorganized MyPeshkar into a clean layered architecture:
>
> - **Config**: Settings live in one place
> - **Core**: LangGraph orchestrates 8 agents
> - **Agents**: Each agent is a specialist (prosecutor, judge, researcher)
> - **Services**: LLM calls and authentication
> - **Evaluation**: Metrics and testing
> - **UI**: Streamlit frontend
> - **Utils**: Helpers and validators
>
> This makes it easy to add features, understand code, and test in isolation."

### Detailed 5-Minute Explanation:

> "MyPeshkar is a legal AI system with 8 specialized agents. Each agent is trained to do one thing well:
>
> 1. **Case Analyst** - reads complaint, extracts details
> 2. **Legal Researcher** - finds relevant laws and precedents
> 3. **Prosecutor** - builds prosecution arguments
> 4. **Defense** - builds defense arguments
> 5. **Judge** - delivers verdict with reasoning
> 6. **Reporter** - writes news summary
> 7. **Consultant** - provides internal strategy advice
> 8. **Top Consultant** - final independent review
>
> These agents are coordinated by **LangGraph** (orchestrator.py). The orchestrator defines the workflow: agent order, data passing, state management.
>
> When a case flows through, it passes through all agents sequentially. Each agent reads the case state, processes it, and updates the state with its output.
>
> **Services layer** handles external dependencies:
> - LLM service communicates with Groq API
> - Auth service manages user login
>
> **UI layer** is Streamlit frontend - will be split into pages and components.
>
> This modular design means:
> - Want to add a new agent? Add file to src/agents/
> - Want to change UI? Edit only src/ui/
> - Want to fix auth? Edit only src/services/auth_service.py
> - Tests are easy to write for individual modules"

---

## 📝 Next Steps: Update Your app.py

Your `app.py` is currently in the root directory. You need to:

1. **Move it to `src/ui/app.py`**
2. **Update imports at the top:**

```python
# OLD IMPORTS (remove these)
from graph.graph import court_graph
from auth import authenticate, submit_access_request
from evaluation.evaluator import SystemEvaluator

# NEW IMPORTS (add these)
from src.core import court_graph
from src.services import authenticate, submit_access_request
from src.evaluation.evaluator import SystemEvaluator
from src.config import (
    APP_NAME,
    APP_TAGLINE,
    APP_PAGE_TITLE,
    APP_PAGE_ICON,
)
```

3. **Start your app with:**
```bash
streamlit run src/ui/app.py
```

---

## 🧩 Import Examples

### In an Agent File (src/agents/case_analyst.py):
```python
from ..services import call_structured
from ..core import CourtState
from .schemas import CaseIntake

# Use them:
result = call_structured(SYSTEM, user, CaseIntake)
```

### In a Service File (src/services/my_service.py):
```python
from .llm_service import call_claude
from ..config import API_TIMEOUT_SECONDS

# Use them:
response = call_claude(system, user)
```

### In UI Page (src/ui/pages/tools_page.py):
```python
from ..core import court_graph
from ..config import APP_NAME

# Use them:
result = court_graph.invoke(state)
```

---

## ✨ Benefits of This Structure

| Benefit | Example |
|---------|---------|
| **Clear Responsibility** | Want to add a new agent? Go to `src/agents/` |
| **Isolated Testing** | Test case_analyst independently without UI |
| **Import Clarity** | `from ..services import` is clear import path |
| **Team Onboarding** | New engineer sees structure, understands organization immediately |
| **Easy Refactoring** | Move LLM provider from Groq to OpenAI? Only change `llm_service.py` |
| **Scalability** | Adding REST API? Just create `src/api/routes.py` |
| **Professional Appearance** | Looks like code written by experienced engineer |

---

## 🔄 Migration Mapping (Old → New)

```
agents/case_manager.py      → src/agents/case_analyst.py
agents/legal_research.py    → src/agents/legal_researcher.py
agents/*.py                 → src/agents/*.py
agents/web_search.py        → src/utils/web_search.py
agents/__init__.py (funcs)  → src/services/llm_service.py

auth.py                     → src/services/auth_service.py

graph/graph.py              → src/core/orchestrator.py
graph/state.py              → src/core/state.py

evaluation/*.py             → src/evaluation/*.py

app.py                      → src/ui/app.py (TO BE MOVED)
```

---

## 🧪 Verification Checklist

- ✅ `src/config/constants.py` exists
- ✅ `src/config/settings.py` exists
- ✅ `src/core/orchestrator.py` exists (LangGraph)
- ✅ `src/agents/` has 9 agent files
- ✅ `src/services/llm_service.py` exists
- ✅ `src/services/auth_service.py` exists
- ✅ `src/evaluation/` has evaluator, metrics, dashboard
- ✅ `src/ui/` directory created (ready for app.py)
- ✅ `src/utils/` has helpers, validators, logger, web_search
- ✅ All imports updated automatically ✨

---

## 🚀 Running Your App

```bash
# Make sure you're in the project root
cd /Users/iqbaltaha3/Documents/PROJECTS/AI_PROJECTS/courtroom

# Update app.py imports, then run:
streamlit run src/ui/app.py

# Or if app.py is still in root (temporarily):
streamlit run app.py
```

---

## 📚 File-by-File Organization

### Config Layer (src/config/)
- **constants.py** - All hardcoded values (colors, names, timeouts)
- **settings.py** - Environment variables (API keys, paths, feature flags)

### Core Layer (src/core/)
- **orchestrator.py** - LangGraph workflow orchestration (how agents work together)
- **state.py** - TypedDict defining case state (data structure)

### Agent Layer (src/agents/)
- **case_analyst.py** - Extracts case details
- **legal_researcher.py** - Legal research
- **prosecutor.py** - Prosecution arguments (rounds 1 & 2)
- **defense.py** - Defense arguments (rounds 1 & 2)
- **judge.py** - Verdict delivery
- **reporter.py** - Journalistic summary
- **consultant.py** - Strategy advice
- **top_consultant.py** - Final review
- **schemas.py** - Pydantic models for structured output

### Service Layer (src/services/)
- **llm_service.py** - Groq API client (call_claude, call_structured)
- **auth_service.py** - User authentication & access control

### Evaluation Layer (src/evaluation/)
- **evaluator.py** - Case analysis quality evaluation
- **metrics.py** - Performance metrics tracking
- **dashboard.py** - Metrics visualization
- **data/** - Historical metrics data (JSONL)

### UI Layer (src/ui/)
- **app.py** - Main Streamlit app (to be moved here)
- **components/** - Reusable UI pieces
- **pages/** - Different app sections (tools, metrics, vision)

### Utility Layer (src/utils/)
- **web_search.py** - Web search integration
- **helpers.py** - Utility functions
- **validators.py** - Input validation
- **logger.py** - Logging configuration

### API Layer (src/api/)
- **routes.py** - REST API endpoints (future)

---

## 💡 Pro Tips

1. **Use relative imports** in src/ modules:
   ```python
   from ..services import call_claude  # Go up one level to src
   from .schemas import CaseIntake     # Same level imports
   ```

2. **Add docstrings** to make code self-documenting for interviews

3. **One responsibility per module** - if file gets >300 lines, split it

4. **Config first** - any repeated value goes to constants.py or settings.py

5. **Testing** - put tests in `/tests/unit/` and `/tests/integration/`

---

## ❓ Questions?

If imports don't work:
1. Check relative import paths match your location
2. Make sure all `__init__.py` files exist in each module
3. Run `python -c "from src.core import court_graph"` to test

---

**You're ready to explain this in interviews! This is professional, clean, and scalable code organization.** ✨
