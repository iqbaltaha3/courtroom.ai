# MyPeshkar Modular Structure - Interview Cheat Sheet

## 30-Second Pitch

"MyPeshkar is a legal AI system. I organized the code into 7 layers for clarity: **config** (settings), **core** (workflow), **agents** (8 AI specialists), **services** (APIs), **evaluation** (metrics), **UI** (Streamlit), and **utils** (helpers).

Each layer has one job. This makes it easy to understand, test, and extend."

---

## The Layers (Memorize These)

| Layer | Purpose | Example |
|-------|---------|---------|
| **Config** | Settings & constants | Colors, API keys, app name |
| **Core** | Workflow orchestration | LangGraph, case state |
| **Agents** | AI specialists | Prosecutor, Judge, Researcher |
| **Services** | External APIs & auth | LLM calls, user login |
| **Evaluation** | Testing & metrics | Performance tracking |
| **UI** | User interface | Streamlit app, pages |
| **Utils** | Helper functions | Web search, validators |

---

## The 8 Agents (Know These)

1. **Case Analyst** - Extract case details
2. **Legal Researcher** - Find laws & precedents
3. **Prosecutor** - Build prosecution case
4. **Defense** - Build defense case
5. **Judge** - Deliver verdict
6. **Reporter** - Write news summary
7. **Consultant** - Strategy advice
8. **Top Consultant** - Final review

**They work in this order** (defined in orchestrator.py)

---

## Three Things to Point Out

### 1. Separation of Concerns
"Each folder has ONE responsibility. Want to change auth? Edit only `auth_service.py`. Want to add agent? Add to `agents/` folder."

### 2. Scalability
"If I need to add REST API? Just create `api/routes.py`. Change LLM provider? Just update `llm_service.py`. Easy."

### 3. Testability
"I can test case_analyst independently without running the whole app. Just import and test the function. No UI needed."

---

## Import Patterns

### In agents (src/agents/case_analyst.py):
```python
from ..services import call_structured  # Up to src/services
from ..core import CourtState           # Up to src/core
```

### In services (src/services/llm_service.py):
```python
from ..config import API_TIMEOUT        # Up to src/config
```

### In UI (src/ui/app.py):
```python
from src.core import court_graph
from src.services import authenticate
```

---

## Key Files to Know

| File | What It Does |
|------|-------------|
| `src/config/constants.py` | All colors, names, timeouts |
| `src/config/settings.py` | Environment variables, API keys |
| `src/core/orchestrator.py` | Defines agent workflow & sequence |
| `src/core/state.py` | Case state TypedDict (data structure) |
| `src/agents/case_analyst.py` | First agent - case extraction |
| `src/services/llm_service.py` | Groq API client |
| `src/services/auth_service.py` | User authentication |
| `src/evaluation/evaluator.py` | Quality metrics |
| `src/ui/app.py` | Main Streamlit app |

---

## Interview Q&A

**Q: How do agents communicate?**
A: Through the case state. Each agent reads state, processes, updates it. LangGraph orchestrator defines the sequence.

**Q: What if I need to change the LLM?**
A: Only change `src/services/llm_service.py`. Groq → OpenAI? One file edit.

**Q: How do you test this?**
A: Each module is independent. Test `case_analyst.run()` alone with mock state. Test `llm_service.call_claude()` with mock API responses.

**Q: Why not put everything in one file?**
A: Hard to navigate 5000-line file. Hard to test. Multiple people can't work on same file. This is professional software structure.

**Q: How do you onboard a new engineer?**
A: "Read this folder structure. Each folder has one purpose. Agents do legal analysis. Services handle APIs. UI is Streamlit. Done."

---

## Diagram to Draw on Whiteboard

```
┌─────────────────────┐
│   UI (Streamlit)    │ User interacts here
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Core (Orchestrator)│ Coordinates agents
└──────────┬──────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼──┐   ┌─────▼────┐
│Agents│   │Services  │ LLM calls
└──────┘   └──────────┘
    │             │
    └─────┬───────┘
          │
┌─────────▼──────────┐
│  Config + Utils    │ Shared helpers
└────────────────────┘
```

---

## Things NOT to Say

❌ "I used AI to generate this structure"
❌ "This is industry standard" (it's good but not unique)
❌ "I organized it perfectly" (always room for improvement)

---

## Things TO Say

✅ "I organized by responsibility - each folder has one job"
✅ "This makes it easy to test, extend, and onboard new developers"
✅ "Each layer is independent - can swap implementations"
✅ "All imports follow a clear pattern - relative imports within src/"

---

## Before Interview

- [ ] Run `tree src -L 3` to see structure
- [ ] Read one agent file to understand pattern
- [ ] Check `orchestrator.py` to see agent sequence
- [ ] Know the 8 agent names
- [ ] Practice the 30-second pitch

---

## Red Flags to Avoid

❌ Getting confused about agent order (look at orchestrator.py)
❌ Not knowing what's in config/ vs services/
❌ Saying "I separated concerns" without explaining how
❌ Not being able to point to a file when asked

---

**You've got this! Clean code = confident interview.** ✨
