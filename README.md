# ⚖️ Courtroom AI — Multi-Agent Legal Simulation

A sophisticated multi-agent system that simulates adversarial courtroom proceedings under Indian law. This system processes a complaint through a graph of specialized AI agents, each playing a distinct role in legal analysis and argumentation, ultimately producing a structured judicial verdict with comprehensive reasoning.

**Status**: Production-ready | **Language**: Python 3.10+ | **Framework**: LangGraph + Streamlit + FastAPI

---

## 📖 Table of Contents

1. [Core Concept & Philosophy](#core-concept--philosophy)
2. [System Architecture](#system-architecture)
3. [Data Model & State Management](#data-model--state-management)
4. [Agent Specifications](#agent-specifications)
5. [Evaluation Framework](#evaluation-framework)
6. [Technology Stack & Rationale](#technology-stack--rationale)
7. [Setup & Installation](#setup--installation)
8. [Running the System](#running-the-system)
9. [Design Decisions & Trade-offs](#design-decisions--trade-offs)
10. [API Reference](#api-reference)
11. [Extending the System](#extending-the-system)

---

## Core Concept & Philosophy

### The Vision

Courtroom AI reimagines legal analysis through **adversarial simulation**. Rather than analyzing a case in isolation, the system orchestrates a structured debate between specialized AI agents, each armed with distinct expertise and incentives:

- **Prosecution** advances the strongest possible case for guilt
- **Defense** systematically challenges the prosecution's narrative
- **Judge** weighs evidence impartially and renders a reasoned verdict
- **Researchers** identify applicable law and precedent
- **Consultants** provide expert advisory throughout

### Why This Approach?

Traditional NLP-based legal analysis often produces monolithic summaries. Adversarial simulation offers several advantages:

| Aspect | Traditional Analysis | Courtroom AI |
|--------|---------------------|-------------|
| **Bias** | Single perspective | Competing perspectives force balanced analysis |
| **Argumentation** | Passive extraction | Active reasoning under pressure to persuade/defend |
| **Legal Reasoning** | Surface-level | Deep engagement with statutes, precedent, factual gaps |
| **Explainability** | "Here's what I found" | "Here's why I decided this" (judge's reasoning) |
| **Audit Trail** | Unclear | Clear: complaint → analysis → debate → verdict |

---

## System Architecture

### High-Level System Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     COURTROOM AI SYSTEM                         │
└─────────────────────────────────────────────────────────────────┘

                        ┌──────────────┐
                        │   UI LAYER   │
                        └──────┬───────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
      ┌────▼─────┐      ┌──────▼──────┐    ┌──────▼──────┐
      │ Streamlit │      │   FastAPI   │    │  CLI Tests  │
      │    UI     │      │   Server    │    │             │
      └────┬─────┘      └──────┬──────┘    └─────────────┘
           │                   │
           │    ┌──────────────┼──────────────┐
           │    │              │              │
           └────┼──────┬───────┴─────┬────────┘
                │      │             │
         ┌──────▼──────▼──────┐  ┌───▼──────────┐
         │   LANGGRAPH        │  │  Evaluation  │
         │   State Machine    │  │   Module     │
         │   (Graph Executor) │  │              │
         └────────┬───────────┘  └───┬──────────┘
                  │                  │
     ┌────────────┴──────────────────┴────────────┐
     │                                             │
     │     AGENT NETWORK (Sequential Pipeline)     │
     │                                             │
     │  1. Case Manager        ──►  Extract entities & facts
     │  2. Legal Research      ──►  Find applicable laws
     │  3. Internal Consultant ──►  Advisory analysis
     │  4. Prosecutor R1       ──►  Opening argument
     │  5. Defense R1          ──►  Counter-argument
     │  6. Prosecutor R2       ──►  Closing argument
     │  7. Defense R2          ──►  Final rebuttal
     │  8. Judge               ──►  Render verdict
     │  9. Reporter            ──►  Case summary
     │ 10. Consultant Sparrow  ──►  Final review
     │                                             │
     └────────────┬─────────────────────────────────┘
                  │
         ┌────────▼─────────────┐
         │  OUTPUT & STORAGE    │
         │                      │
         │ • PDF Report         │
         │ • Markdown Export    │
         │ • Metrics Database   │
         │ • Case Archive       │
         └──────────────────────┘
```

### Data Flow: From Complaint to Verdict

```
COMPLAINT INPUT
     │
     │ (text or file upload)
     ▼
┌──────────────────────┐
│  Case Manager Agent  │────────► Extract: accused, victim, facts, allegation
│  (Structured NLP)    │          Output: CaseIntake dataclass
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│ Legal Research Agent │────────► Search: applicable sections, precedents
│  (Law Database)      │          Output: LegalResearch dataclass
└──────────────────────┘
     │
     ▼
┌──────────────────────┐
│Internal Consultant   │────────► Advise: strategy, evidence gaps
│  (Advisory)          │          Output: Free-form text
└──────────────────────┘
     │
     ├──────────────────────────────────┐
     │                                  │
     ▼                                  ▼
┌──────────────────────┐    ┌──────────────────────┐
│ Prosecutor R1        │    │ Defense R1           │
│ (Opening Argument)   │    │ (Counter Argument)   │
└──────────────────────┘    └──────────────────────┘
     │                                  │
     └──────────────┬───────────────────┘
                    │
     ┌──────────────┴───────────────────┐
     │                                  │
     ▼                                  ▼
┌──────────────────────┐    ┌──────────────────────┐
│ Prosecutor R2        │    │ Defense R2           │
│ (Closing Argument)   │    │ (Final Rebuttal)     │
└──────────────────────┘    └──────────────────────┘
     │                                  │
     └──────────────┬───────────────────┘
                    │
                    ▼
            ┌──────────────────────┐
            │   Judge Agent        │◄──── Input: All previous outputs + legal research
            │ (Verdict Reasoning)  │
            └──────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
   Verdict      Confidence  Reasoning
   (Guilty/     (0-100%)    (Detailed
    Not Guilty/             Legal
    Partial)                Analysis)
        │
        ▼
┌──────────────────────┐
│  Reporter Agent      │────────► Journalistic summary + headline
│  (Case Summary)      │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│ Consultant Sparrow   │────────► Final holistic review
│ (Meta-Analysis)      │
└──────────────────────┘
        │
        ▼
    OUTPUTS:
    • judge_verdict (structured)
    • report (journalistic)
    • confidence (0-100)
    • reasoning (detailed)
    • headline (case summary)
```

### Component Interaction Graph

```
User Input (Complaint)
    ↓
Streamlit Frontend
    ↓
LangGraph State Machine ─────────┐
    ├─► Agent 1: Case Manager    │
    ├─► Agent 2: Legal Research  │
    ├─► Agent 3: Consultant      │
    ├─► Agents 4-7: Debate       │
    ├─► Agent 8: Judge           ├──► Evaluation Module
    ├─► Agent 9: Reporter        │
    └─► Agent 10: Sparrow        │
        ↓                        │
    Final State ────────────────┘
        ├─► Report Generation
        │   ├─ PDF (ReportLab)
        │   └─ Markdown
        │
        └─► Metrics Collection
            ├─ JSONL Database
            └─ Dashboard Visualization
```

---

## Data Model & State Management

### CourtState TypedDict (graph/state.py)

The entire simulation state is managed by a single immutable dictionary called `CourtState`. This design choice ensures:

- **Single source of truth**: All agents read from and write to the same state
- **Immutability by convention**: Each agent receives state, returns updates (LangGraph merges)
- **Type safety**: TypedDict with Optional fields prevents runtime errors
- **Explicit contracts**: Every agent's input/output is visible in the type definition

```python
class CourtState(TypedDict):
    # Input
    complaint: str
    
    # Case Analysis (Agent 1)
    case_intake: Optional[dict]    # CaseIntake.model_dump()
    accused: Optional[str]
    victim: Optional[str]
    facts: Optional[str]
    
    # Legal Research (Agent 2)
    legal_research: Optional[dict]  # LegalResearch.model_dump()
    laws: Optional[str]
    sections_applied: Optional[str]
    
    # Debate (Agents 4-7)
    pros_r1: Optional[str]  # Prosecution Round 1
    def_r1: Optional[str]   # Defense Round 1
    pros_r2: Optional[str]  # Prosecution Round 2
    def_r2: Optional[str]   # Defense Round 2
    
    # Verdict (Agent 8)
    judge_verdict: Optional[dict]   # JudgeVerdict.model_dump()
    verdict: Optional[str]          # Full text verdict
    verdict_short: Optional[str]    # "Guilty" / "Not Guilty" / "Partially Liable"
    confidence: Optional[int]       # 0-100
    
    # Advisory (Agents 3, 10)
    consultant: Optional[str]       # Internal analysis
    top_consultant: Optional[str]   # Final review
    
    # Report (Agent 9)
    headline: Optional[str]
    report: Optional[str]
```

### Structured vs. Free-Form Outputs

**Why this hybrid approach?**

Some agents produce **structured outputs** (Pydantic dataclasses):
- **Case Manager, Legal Research, Judge**: These require discrete fields (accused, verdict, sections)
- Reasoning: Downstream agents and UI components need to parse/display specific fields
- Tool: `call_structured()` enforces schema via LLM function calling

Other agents produce **free-form text**:
- **Prosecutor, Defense, Reporter, Consultants**: These produce persuasive/narrative prose
- Reasoning: Rigid schemas degrade writing quality; these are read by humans, not parsed
- Tool: `call_claude()` for text generation without schema constraint

This hybrid design balances **structure (for computation)** with **quality (for readability)**.

### Storage Patterns

```
Structured (JSON):
├── case_intake
│   ├── accused: str
│   ├── victim: str
│   ├── facts: list[str]
│   └── missing_information: list[str]
├── legal_research
│   ├── applicable_sections: list[ApplicableSection]
│   ├── precedents: list[Precedent]
│   └── evidentiary_notes: list[str]
└── judge_verdict
    ├── verdict: "Guilty" | "Not Guilty" | "Partially Liable"
    ├── confidence: int (0-100)
    ├── reasoning: str
    └── sections_applied: list[str]

Free-form (String):
├── pros_r1, pros_r2: Prosecution arguments
├── def_r1, def_r2: Defense arguments
├── consultant: Internal advisory
├── top_consultant: Meta-analysis
├── report: Journalistic summary
└── headline: Case title
```

---

## Agent Specifications

### 1. Case Manager Agent
**Purpose**: Extract entities and facts from unstructured complaint text

**Input**: `complaint: str`

**Output**:
```python
CaseIntake(
    accused: str              # Who is accused
    victim: str               # Who is the alleged victim
    allegation: str           # One-line summary of allegation
    offences: str             # What crimes are suggested
    jurisdiction: str         # Which court has jurisdiction
    facts: list[str]          # Chronological material facts
    missing_information: list[str]  # What's absent that matters
)
```

**Why Structured?** Downstream agents need to reference specific entities (e.g., judge needs accused name for verdict). UI displays these fields in a card layout.

**Implementation** (`agents/case_manager.py`):
```python
def run_case_manager(state: CourtState) -> dict:
    system_prompt = """You are a legal case intake specialist..."""
    user_input = state['complaint']
    result: CaseIntake = call_structured(system_prompt, user_input, CaseIntake)
    return {"case_intake": result.model_dump()}
```

---

### 2. Legal Research Agent
**Purpose**: Identify applicable laws, precedents, and evidentiary principles

**Input**: `complaint: str`, `case_intake: dict`

**Output**:
```python
LegalResearch(
    applicable_sections: list[ApplicableSection]
        # Each: (section: "Section 316, BNS", act: "Bharatiya Nyaya Sanhita", relevance: "...")
    precedents: list[Precedent]
        # Each: (case_name: "...", court: "...", year: "...", relevance: "...")
    evidentiary_notes: list[str]
        # Notes on Bharatiya Sakshya Adhiniyam (BSA) applicability
    unsettled_questions: list[str]
        # Areas of legal uncertainty
)
```

**Why This Design?**

- **Section-level granularity**: Judge can cite specific sections in verdict, prosecutors/defense can challenge specific citations
- **Precedent traceability**: Allows audit trail of legal reasoning
- **Evidentiary module awareness**: Modern Indian procedural law (BSA 2023) differs from old Evidence Act; this captures nuances
- **Unsettled questions flag**: Highlights genuine legal ambiguity rather than pretending certainty

**Context**: Agents receive this research before debating, ensuring fact-checked law references.

---

### 3. Prosecution Agent (Rounds 1 & 2)
**Purpose**: Build the strongest possible case for guilt

**Input**: Full state including complaint, case facts, legal research, defense arguments

**Output**: Free-form persuasive prose

**Philosophy**: The prosecutor must:
1. Establish elements of the alleged crime
2. Connect facts to legal provisions
3. Anticipate and refute defense arguments (especially in R2)
4. Maintain credibility through factual grounding

**Why Not Structured?** Persuasive writing requires narrative flow, rhetorical strategy, and emotional resonance. Schema constraints would force artificial segmentation.

**Round 1 (Opening)**: Sets the narrative, establishes timeline, introduces key evidence
**Round 2 (Closing)**: Responds to defense, synthesizes evidence, applies law to facts

---

### 4. Defense Agent (Rounds 1 & 2)
**Purpose**: Challenge the prosecution's case systematically

**Input**: Full state including prosecution arguments, legal research

**Output**: Free-form counter-arguments

**Defense Strategy**:
1. Challenge factual assumptions (burden of proof on prosecution)
2. Highlight gaps in evidence
3. Offer alternative interpretations of facts
4. Challenge applicability of cited law sections
5. Emphasize defendant's presumption of innocence

**Round 1 (Opening)**: Presents counter-narrative and challenges to prosecutor's case
**Round 2 (Rebuttal)**: Addresses prosecutor's Round 2 closing arguments

---

### 5. Judge Agent
**Purpose**: Render an impartial verdict with detailed reasoning

**Input**: 
- Complaint
- Case facts (from Case Manager)
- Legal research (sections, precedents)
- Both sides' arguments (prosecution R1/R2, defense R1/R2)

**Output**:
```python
JudgeVerdict(
    findings: str                    # 2-3 sentences: what facts are established
    prosecution_assessment: str      # 1-2 sentences: judge's view of prosecution case
    defense_assessment: str          # 1-2 sentences: judge's view of defense
    reasoning: str                   # 3-5 sentences: why verdict follows from law + facts
    verdict: Literal["Guilty", "Not Guilty", "Partially Liable"]
    sections_applied: list[str]      # Which sections justified verdict
    probable_punishment: str         # Jail, fine, compensation implications
    confidence: int                  # 0-100 confidence in this verdict
)
```

**Why Confidence is Critical**:
- **0-49**: Missing facts, thin evidence, genuine uncertainty (verdict may be overturned on appeal)
- **50-69**: Mixed facts or unsettled law; verdict is reasonable but not inevitable
- **70-89**: Clear facts and settled law; verdict is well-grounded
- **90-100**: Facts are undisputed, law is clear, verdict is virtually compelled

**Judicial Temperament** (from system prompt):
- Strictly neutral, no favoritism
- Shows reasoning, not mere conclusion
- Distinguishes inapplicable authorities
- Never invents evidence; bases conclusions only on material provided

---

### 6. Reporter Agent
**Purpose**: Craft a journalistic case summary

**Input**: Full verdict and case details

**Output**:
```
headline: str     # E.g., "Court Convicts Accused in Theft Case; Sets Bail Pending Appeal"
report: str       # 200-300 word journalistic summary
```

**Style**: Neutral, factual, accessible to non-lawyers. Emphasizes key facts and verdict without legal jargon.

---

### 7. Consultant & Consultant Sparrow (Top Consultant)
**Purpose**: Internal advisory before debate, and holistic meta-analysis after verdict

**Consultant** (pre-debate):
- Analyzes case strategy
- Flags evidence gaps
- Advises both sides implicitly

**Consultant Sparrow** (post-verdict):
- Reviews entire proceeding
- Assesses verdict coherence
- Flags potential appeal grounds

---

## Evaluation Framework

### Multi-Dimensional Quality Assessment

The evaluation system measures quality across **8 categories** with **20+ individual metrics**, each scored 0-100:

```
┌─────────────────────────────────────────────────────────┐
│         EVALUATION FRAMEWORK (8 CATEGORIES)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. CASE ANALYSIS (20% weight)                         │
│     ├─ Case Extraction Completeness                     │
│     ├─ Fact Accuracy                                    │
│     └─ Entity Recognition Accuracy                      │
│                                                         │
│  2. LEGAL RESEARCH (25% weight)                        │
│     ├─ Applicable Sections Relevance                    │
│     ├─ Precedent Relevance                              │
│     └─ Legal Research Completeness                      │
│                                                         │
│  3. DEBATE ARGUMENTATION (25% weight)                  │
│     ├─ Prosecution Coherence                            │
│     ├─ Defense Coherence                                │
│     └─ Argument Strength (Balance)                      │
│                                                         │
│  4. VERDICT QUALITY (30% weight)                       │
│     ├─ Justification Quality                            │
│     ├─ Confidence Calibration                           │
│     ├─ Reasoning Clarity                                │
│     ├─ Precedent Adherence                              │
│     └─ Consistency (both sides addressed)               │
│                                                         │
└─────────────────────────────────────────────────────────┘

OVERALL SCORE = (Case×0.20) + (Legal×0.25) + (Debate×0.25) + (Verdict×0.30)
Range: 0-100 (90+ excellent, 70-89 good, 55-69 acceptable, <55 poor)
```

### Evaluation Metrics Collection

```
metrics_history.jsonl (Append-only log)
├─ Timestamp-indexed
├─ One JSON object per line (immutable audit trail)
└─ Fields: case_id, overall_quality_score, all 20+ metrics, verdict, confidence

summary.json (Live aggregates)
├─ Total cases analyzed
├─ Average score overall + by component
├─ Verdict distribution (Guilty / Not Guilty / Partial)
├─ Confidence statistics (mean, std, distribution)
└─ Performance metrics (execution time by agent)
```

### Evaluation vs. Judgment

**Important distinction**:
- **Judge's Verdict**: "What is the court's decision?" (Agent 8's output)
- **System Evaluation**: "How good was this verdict?" (Evaluation module's assessment)

The evaluation module doesn't judge guilt/innocence; it assesses whether the verdict is well-reasoned, internally consistent, and grounded in presented evidence.

**Example**:
- Judge verdict: "Not Guilty" (low confidence: 35%)
- Evaluation assessment: Verdict may be questionable given available evidence, appeals likely

---

## Technology Stack & Rationale

### Core Technologies

| Layer | Technology | Why Chosen | Alternatives Rejected |
|-------|-----------|-----------|----------------------|
| **State Machine** | LangGraph | Native multi-agent orchestration with streaming | Airflow (overly complex), custom event system (reinvents wheel) |
| **LLM Provider** | Anthropic Claude | Advanced reasoning, function calling, long context | GPT-4 (cost), Llama (local latency) |
| **UI** | Streamlit | Rapid prototyping, native session state, minimal boilerplate | Django/React (heavyweight), Gradio (limited) |
| **API** | FastAPI | Async support, automatic OpenAPI docs, streaming with SSE | Flask (no async), Express.js (wrong language) |
| **PDF Generation** | ReportLab | Programmatic control, wrapped text handling, no external deps | Weasyprint (heavy), pandoc (shell dependency) |
| **Visualization** | Plotly | Interactive charts, client-side rendering, no server overhead | Matplotlib (static only), D3.js (overkill) |
| **Data Export** | Pandas + CSV | Standard format, easy import to Excel/R/Python | Custom JSON (nonstandard), Parquet (over-engineering) |

### Why LangGraph Over Custom State Machine?

```
Custom State Machine:
├─ Pros: Full control, minimal dependencies
└─ Cons: 
   ├─ Must implement agent sequencing manually
   ├─ Must handle streaming updates
   ├─ Must implement state merging logic
   ├─ Must debug edge cases (circular refs, state corruption)
   └─ Maintenance burden

LangGraph:
├─ Pros:
   │  ├─ Built for multi-agent workflows
   │  ├─ Native streaming (stream_mode="updates")
   │  ├─ Automatic state merging per LangChain StateGraph spec
   │  ├─ Production-tested (LangChain ecosystem)
   │  └─ Built-in persistence (snapshots, checkpoints)
└─ Cons: Slight learning curve, dependency on LangChain
```

### Why Structured + Free-form Hybrid?

```
All Structured:
├─ Pro: Easy to parse and aggregate
└─ Con: Forces artificial schema onto prose (quality loss)

All Free-form:
├─ Pro: Natural writing quality
└─ Con: Impossible to extract judicial reasoning programmatically

Hybrid (This Project):
├─ Structured where needed (entities, verdict, scores)
├─ Free-form where needed (debate arguments, narrative)
└─ Best of both worlds
```

---

## Setup & Installation

### Prerequisites

- **Python 3.10+** (tested on 3.10, 3.11, 3.12)
- **API Keys**: 
  - `ANTHROPIC_API_KEY` (for Claude via Anthropic)
  - Or: `GOOGLE_API_KEY` (for Gemini via Google AI)
- **Disk Space**: ~500MB for dependencies + evaluation data

### Installation Steps

1. **Clone and navigate**:
   ```bash
   cd /path/to/courtroom
   ```

2. **Create virtual environment**:
   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # or: .venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   # Create .env file in project root
   cat > .env << EOF
   ANTHROPIC_API_KEY=sk-ant-...
   # or:
   GOOGLE_API_KEY=AIzaS...
   EOF
   ```

5. **Verify setup**:
   ```bash
   python -c "from agents import call_structured; print('✓ Setup OK')"
   ```

---

## Running the System

### Option 1: Streamlit UI (Interactive)

**Best for**: Demonstrations, single-case analysis, learning the system

```bash
streamlit run app.py
```

Then:
1. Open http://localhost:8501
2. Enter complaint text or upload .txt/.pdf file
3. Click "Begin Simulation"
4. Watch streaming execution in real-time
5. Download PDF/Markdown report
6. View metrics in "📊 Metrics" tab

**Architecture**:
```
User Input
    ↓
[Streamlit Session State]
    ├─ case_state: CourtState dict
    ├─ stream_iter: LangGraph stream iterator
    ├─ node_times: execution timing
    └─ evaluator: SystemEvaluator instance
    ↓
[Streaming Loop]
    ├─ for each update in graph.stream():
    │   ├─ merge update into case_state
    │   ├─ record execution time
    │   └─ call st.rerun() (UI refresh)
    ├─ on StopIteration: auto-evaluate
    └─ display final verdict + metrics
    ↓
[Report Generation]
    ├─ PDF download (ReportLab)
    └─ Markdown download (raw text)
```

### Option 2: FastAPI Server (Batch/Integration)

**Best for**: Production deployment, batch processing, programmatic integration

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**Endpoints**:

1. **POST /simulate** (blocking):
   ```json
   {
     "complaint": "The accused stole a bicycle...",
     "model": "claude"
   }
   ```
   Returns: `{ "verdict": "...", "confidence": 85, ... }`

2. **POST /simulate/stream** (streaming):
   Returns: Server-Sent Events (SSE) stream of node updates
   ```
   data: {"node": "case_manager", "partial": {...}}
   data: {"node": "legal_research", "partial": {...}}
   ...
   ```

**Use Case Example**:
```python
import requests

response = requests.post(
    "http://localhost:8000/simulate",
    json={"complaint": "..."}
)
result = response.json()
print(f"Verdict: {result['verdict_short']}")
print(f"Confidence: {result['confidence']}%")
```

### Option 3: Direct Python (Testing/Development)

```python
from graph.graph import court_graph
from evaluation.evaluator import SystemEvaluator

complaint = "The accused is charged with theft..."

# Execute graph
state = {"complaint": complaint}
final_state = court_graph.invoke(state)

# Evaluate
evaluator = SystemEvaluator()
metrics = evaluator.evaluate_case(final_state, execution_times={})

print(f"Verdict: {final_state['verdict_short']}")
print(f"Quality: {metrics.overall_quality_score:.1f}/100")
```

---

## Design Decisions & Trade-offs

### Decision 1: Sequential Pipeline vs. Parallel Debate

**Chosen**: Sequential (Prosecutor R1 → Defense R1 → Prosecutor R2 → Defense R2)

**Why?**
- **Logical flow**: Each argument builds on the previous
- **Reduced hallucination**: Agents see the actual prior arguments, not summaries
- **Easier debugging**: Failure at step N doesn't cascade to parallel branches
- **Streaming UX**: Users see progress linearly (not all at once)

**Alternative considered**: Parallel prosecution/defense (simultaneous arguments)
- **Rejected**: Arguments would be based on old facts, less coherent

---

### Decision 2: Structured Judge Verdict

**Chosen**: JudgeVerdict Pydantic model with strict fields

**Why?**
- **Audit trail**: Each component (reasoning, confidence, sections) is separately extractable
- **Downstream integration**: Evaluation module needs confidence as an integer
- **Explainability**: App displays findings, reasoning, and assessment in separate card sections
- **Legal compliance**: Ensures verdict includes required judicial elements

**Alternative considered**: Free-form verdict text
- **Rejected**: Can't extract confidence score reliably from prose; no audit trail

---

### Decision 3: Confidence Score 0-100 (Not Binary)

**Chosen**: Integer confidence, contextualized in system prompt

**Why?**
- **Nuance**: "70% confident" means different thing than "90% confident"
- **Appeal risk**: Quantifies verdict fragility (low confidence = likely appeal ground)
- **Evaluation metric**: Calibration analysis shows if model is overconfident/underconfident

**System Prompt Section**:
```
CONFIDENCE SCORE (0-100):
• 90-100: Facts clear, law settled, verdict compelled by evidence
• 70-89: Mostly clear, some ambiguity remains
• 50-69: Mixed facts/unsettled law; verdict reasonable but not inevitable
• 0-49: Critical facts missing, evidence thin, or highly uncertain
```

---

### Decision 4: Evaluation Module as Post-Hoc Analysis

**Chosen**: Evaluate after verdict is rendered

**Why?**
- **Independence**: Evaluation not visible to Judge agent (no feedback loops)
- **Fairness**: Judge doesn't optimize for "good evaluation scores"
- **Simplicity**: Single pass through case

**Alternative considered**: Evaluation during execution (real-time feedback)
- **Rejected**: Would bias Judge toward "safe" verdicts; reduces decisiveness

---

### Decision 5: Metrics Stored in JSONL (Append-Only)

**Chosen**: `evaluation/data/metrics_history.jsonl` (one JSON per line)

**Why?**
- **Immutable audit trail**: Can't accidentally overwrite past evaluations
- **Streamable**: Can process millions of lines without loading into RAM
- **Standard**: Native support in Pandas, BigQuery, etc.
- **Git-friendly**: Text-based, diff-able

**Alternative considered**: SQLite database
- **Rejected**: Overkill for this use case, adds dependency

---

### Decision 6: Hybrid Pydantic + TypedDict

**Chosen**: 
- Pydantic for structured agent outputs (CaseIntake, LegalResearch, JudgeVerdict)
- TypedDict for state machine (CourtState)

**Why?**
- **Type safety**: TypedDict enforces state shape across agents
- **Serialization**: Pydantic handles JSON serialization automatically
- **Validation**: Pydantic validates LLM outputs (e.g., verdict must be one of 3 values)
- **IDE support**: Both provide autocomplete in modern editors

---

## API Reference

### Streamlit Session State

```python
st.session_state.case_state  # Current CourtState dict
st.session_state.simulation_complete  # bool: simulation finished?
st.session_state.stream_iter  # LangGraph streaming iterator
st.session_state.node_times  # dict: {node_name: execution_time}
st.session_state.evaluator  # SystemEvaluator instance
st.session_state.metrics_recorded  # bool: metrics saved?
```

### LangGraph Streaming

```python
from graph.graph import court_graph

# Stream mode="updates" returns dict of {node_name: partial_state_update}
for event in court_graph.stream(initial_state, stream_mode="updates"):
    for node_name, partial in event.items():
        print(f"{node_name}: {partial}")
```

### Evaluation Module

```python
from evaluation.evaluator import SystemEvaluator

evaluator = SystemEvaluator()

# Evaluate a completed case
metrics = evaluator.evaluate_case(
    state=final_state,
    execution_times=node_times  # dict: {node_name: seconds}
)

# Access metrics
print(metrics.overall_quality_score)  # 0-100
print(metrics.confidence_calibration)  # 0-100
print(metrics.verdict)  # "Guilty" / "Not Guilty" / "Partially Liable"
print(metrics.confidence)  # 0-100

# Get recent cases
recent = evaluator.get_recent_cases(n=10)

# Get summary stats
summary = evaluator.get_metrics_summary()
```

### Metrics Dashboard

```python
from evaluation.dashboard import show_evaluation_dashboard

# In Streamlit context:
show_evaluation_dashboard()  # Renders interactive dashboard with:
# - Summary statistics
# - Quality score trend (line chart)
# - Component breakdown (bar chart)
# - Verdict distribution (pie chart)
# - Execution performance (area chart)
# - Confidence calibration (dual-axis)
# - Recent cases table
# - CSV export button
```

---

## Extending the System

### Adding a New Agent

**Step 1**: Create agent file (`agents/my_agent.py`)
```python
from graph.state import CourtState

def run_my_agent(state: CourtState) -> dict:
    """
    My agent processes X and produces Y.
    """
    input_data = state['some_field']
    output_data = process(input_data)
    return {
        "output_field": output_data,
        # ... any other fields to update state
    }
```

**Step 2**: Register in graph (`graph/graph.py`)
```python
g.add_node("my_agent", run_my_agent)

# Insert into sequence:
g.add_edge("some_previous_agent", "my_agent")
g.add_edge("my_agent", "next_agent_in_pipeline")
```

**Step 3**: Update state schema (`graph/state.py`)
```python
class CourtState(TypedDict):
    # ... existing fields ...
    my_output_field: Optional[str]  # or whatever type
```

**Step 4**: Test
```python
from graph.graph import court_graph

result = court_graph.invoke({"complaint": "test case..."})
assert result['my_output_field'] is not None
```

---

### Customizing Evaluation Metrics

**To add new metric**:

1. Add evaluation method to `evaluation/evaluator.py`:
   ```python
   def _evaluate_new_dimension(self, state: Dict[str, Any]) -> float:
       """Custom metric (0-100)."""
       # ... calculation ...
       return score
   ```

2. Include in `_calculate_overall_score()` weighting

3. Add to `EvaluationMetrics` dataclass (`evaluation/metrics.py`):
   ```python
   @dataclass
   class EvaluationMetrics:
       # ... existing ...
       my_new_metric: float = 0.0
   ```

4. Visualize in dashboard (`evaluation/dashboard.py`):
   ```python
   metrics_df['my_new_metric']  # Add to charts
   ```

---

### Swapping LLM Providers

Current: Anthropic Claude (via `langchain-anthropic`)

To use Google Gemini:

1. Update `agents/__init__.py`:
   ```python
   from langchain_google_genai import ChatGoogleGenerativeAI
   
   llm = ChatGoogleGenerativeAI(model="gemini-pro", api_key=os.getenv("GOOGLE_API_KEY"))
   ```

2. Test a single agent:
   ```bash
   python -c "from agents.case_manager import run_case_manager; ..."
   ```

---

### Integrating with External Legal Databases

The `legal_research` agent currently uses LLM knowledge. To add real law database:

```python
# agents/legal_research.py
def run_legal_research(state: CourtState) -> dict:
    # Call external API
    sections = query_law_database(state['complaint'])  # hypothetical
    precedents = query_precedent_db(state['complaint'])
    
    # Return as before
    return {
        "legal_research": LegalResearch(
            applicable_sections=sections,
            precedents=precedents,
            ...
        ).model_dump()
    }
```

---

## Glossary

| Term | Meaning |
|------|---------|
| **CourtState** | The central TypedDict managing all case data |
| **Node** | An agent in the LangGraph (case_manager, judge, etc.) |
| **Edge** | Connection between nodes (defines execution order) |
| **Stream** | Real-time updates from graph execution |
| **Structured Output** | LLM output conforming to Pydantic schema |
| **Free-form Output** | Unstructured text from LLM (no schema) |
| **Confidence (Verdict)** | Judge's 0-100 confidence in the rendered verdict |
| **Evaluation Score** | System's 0-100 assessment of verdict quality |
| **JSONL** | JSON Lines format (one JSON object per line, newline-delimited) |
| **Precedent Adherence** | Whether verdict cites laws identified by legal research |

---

## Troubleshooting

### Issue: Judge verdict is "Not Guilty" but confidence is 0%

**Cause**: `judge_verdict` dict not properly returned from judge agent

**Fix**: Ensure `agents/judge.py` returns:
```python
return {
    "judge_verdict": {
        "verdict": result.verdict,
        "confidence": result.confidence,  # <-- must be set
        ...
    }
}
```

---

### Issue: Metrics show quality = 32 for all cases

**Cause**: Evaluation module detecting `judge_verdict = None`, returning zeros for verdict quality

**Fix**: See above; ensure judge agent returns judge_verdict dict

---

### Issue: Streamlit stuck at "Court is in session..."

**Cause**: LLM API timeout or network error; stream_iter still trying to fetch next node

**Fix**:
1. Check internet connection
2. Verify API key is set: `echo $ANTHROPIC_API_KEY`
3. Restart Streamlit: `Ctrl+C`, then `streamlit run app.py`

---

## Performance Benchmarks

Typical case analysis (full pipeline):

| Agent | Avg Time | Notes |
|-------|----------|-------|
| Case Manager | 2-3 sec | Entity extraction |
| Legal Research | 3-4 sec | Section + precedent lookup |
| Prosecutor R1 | 4-5 sec | Opening argument |
| Defense R1 | 4-5 sec | Counter-argument |
| Prosecutor R2 | 3-4 sec | Closing argument |
| Defense R2 | 3-4 sec | Rebuttal |
| Judge | 5-7 sec | Verdict reasoning (most complex) |
| Reporter | 2-3 sec | Journalistic summary |
| Consultant Sparrow | 2-3 sec | Meta-analysis |
| **Total** | **28-40 sec** | End-to-end |

**Factors affecting speed**:
- Model temperature & max_tokens (higher = slower)
- LLM provider latency (varies by region)
- Network bandwidth

---

## Contributing

Contributions welcome! Please:

1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Follow code style: Python 3.10+, type hints, docstrings
4. Test: `python -m pytest tests/`
5. Submit PR with description

---

## License

This project is provided as-is for educational and research purposes.

---

## Support

- **Issues**: GitHub Issues (link needed)
- **Discussions**: GitHub Discussions (link needed)
- **Documentation**: See EVALUATION.md, EVALUATION_SETUP.md

---

**Last Updated**: June 2026

**Architecture Version**: 2.0 (Multi-agent with evaluation framework)
