# MyPeshkar Modular Structure - Migration Guide

## Progress Summary

✅ **Completed:**
- `src/config/` - Settings and constants
- `src/core/` - LangGraph orchestrator and state
- `src/services/` - LLM service and auth service
- Directory structure created for all modules

⏳ **Next Steps:**
- Copy and update agent files
- Create UI components and pages
- Create evaluation module
- Update imports throughout

---

## Import Mapping (How Imports Change)

### Old → New Import Paths

```python
# OLD IMPORTS (from agents/)
from agents import call_claude, call_structured
from graph.graph import court_graph
from graph.state import CourtState
from auth import authenticate, submit_access_request
from evaluation.evaluator import SystemEvaluator

# NEW IMPORTS (from src/)
from src.services import call_claude, call_structured
from src.core import court_graph, CourtState
from src.services import authenticate, submit_access_request
from src.evaluation import SystemEvaluator
```

---

## File Movement Checklist

### Agents (8 files)
- [ ] `agents/case_manager.py` → `src/agents/case_analyst.py`
- [ ] `agents/legal_research.py` → `src/agents/legal_researcher.py`
- [ ] `agents/prosecutor.py` → `src/agents/prosecutor.py`
- [ ] `agents/defense.py` → `src/agents/defense.py`
- [ ] `agents/judge.py` → `src/agents/judge.py`
- [ ] `agents/reporter.py` → `src/agents/reporter.py`
- [ ] `agents/consultant.py` → `src/agents/consultant.py`
- [ ] `agents/top_consultant.py` → `src/agents/top_consultant.py`
- [ ] `agents/schemas.py` → `src/agents/schemas.py` (no import changes needed)
- [ ] `agents/web_search.py` → `src/utils/web_search.py`

### Services (already created)
- [x] `auth.py` → `src/services/auth_service.py`
- [x] LLM calls → `src/services/llm_service.py`

### Evaluation
- [ ] `evaluation/evaluator.py` → `src/evaluation/evaluator.py`
- [ ] `evaluation/metrics.py` → `src/evaluation/metrics.py`
- [ ] `evaluation/dashboard.py` → `src/evaluation/dashboard.py`

### UI (needs major refactoring)
- [ ] Extract CSS → `src/ui/components/styles.py`
- [ ] Extract forms → `src/ui/components/forms.py`
- [ ] Tools tab → `src/ui/pages/tools_page.py`
- [ ] Metrics tab → `src/ui/pages/metrics_page.py`
- [ ] Vision tab → `src/ui/pages/vision_page.py`
- [ ] Main app → `src/ui/app.py`

---

## Standard Import Pattern for Agents

When copying agent files, update imports like this:

```python
# At top of agent file, change:
# FROM:
from agents import call_claude, call_structured
from graph.state import CourtState

# TO:
from ..services import call_claude, call_structured
from ..core import CourtState
```

---

## Directory Structure (Final)

```
src/
├── config/
│   ├── __init__.py ✅
│   ├── constants.py ✅
│   └── settings.py ✅
├── core/
│   ├── __init__.py ✅
│   ├── orchestrator.py ✅
│   └── state.py ✅
├── agents/
│   ├── __init__.py ✅
│   ├── case_analyst.py ⏳
│   ├── legal_researcher.py ⏳
│   ├── prosecutor.py ⏳
│   ├── defense.py ⏳
│   ├── judge.py ⏳
│   ├── reporter.py ⏳
│   ├── consultant.py ⏳
│   ├── top_consultant.py ⏳
│   └── schemas.py ⏳
├── services/
│   ├── __init__.py ✅
│   ├── llm_service.py ✅
│   └── auth_service.py ✅
├── ui/
│   ├── __init__.py ⏳
│   ├── app.py ⏳
│   ├── components/
│   │   ├── __init__.py ⏳
│   │   ├── styles.py ⏳
│   │   └── forms.py ⏳
│   └── pages/
│       ├── __init__.py ⏳
│       ├── tools_page.py ⏳
│       ├── metrics_page.py ⏳
│       └── vision_page.py ⏳
├── evaluation/
│   ├── __init__.py ⏳
│   ├── evaluator.py ⏳
│   ├── metrics.py ⏳
│   └── dashboard.py ⏳
├── api/
│   ├── __init__.py ⏳
│   └── routes.py ⏳
└── utils/
    ├── __init__.py ⏳
    ├── helpers.py ⏳
    ├── validators.py ⏳
    ├── logger.py ⏳
    └── web_search.py ⏳
```

---

## Interview Narrative (When Complete)

> "I reorganized MyPeshkar into a clean modular structure with clear separation of concerns:
>
> - **config/**: All settings and constants in one place
> - **core/**: LangGraph workflow orchestration
> - **agents/**: 8 specialized AI agents
> - **services/**: LLM API calls and authentication
> - **ui/**: Streamlit interface organized by page
> - **evaluation/**: Testing and metrics
> - **utils/**: Helper functions and validators
>
> This makes it easy for new team members to understand: each folder has one responsibility, imports are clean and predictable, and adding new features (like a new agent or page) is straightforward.
> 
> The structure follows industry best practices (layered architecture) while staying simple enough to explain in interviews."

