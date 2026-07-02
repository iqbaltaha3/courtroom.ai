"""LangGraph orchestrator - coordinates AI agents in legal case analysis."""
from langgraph.graph import StateGraph, END

# Import state directly to avoid circular imports
from .state import CourtState
from ..agents.case_analyst import run_case_manager
from ..agents.legal_researcher import run_legal_research
from ..agents.consultant import run_consultant
from ..agents.top_consultant import run_top_consultant
from ..agents.prosecutor import run_prosecutor_r1, run_prosecutor_r2
from ..agents.defense import run_defense_r1, run_defense_r2
from ..agents.judge import run_judge
from ..agents.reporter import run_reporter


def build_graph() -> StateGraph:
    """Build the LangGraph workflow for case analysis.
    
    Orchestrates 10 agents in sequence:
    1. Case Manager - Extract case details
    2. Legal Researcher - Find relevant laws and precedents
    3. Consultant - Internal strategy review
    4. Prosecutor Round 1 - Opening argument
    5. Defense Round 1 - Opening response
    6. Prosecutor Round 2 - Closing argument
    7. Defense Round 2 - Closing response
    8. Judge - Verdict and reasoning
    9. Reporter - Generate news summary
    10. Top Consultant - Final review
    """
    g = StateGraph(CourtState)

    # Register nodes
    g.add_node("case_manager", run_case_manager)
    g.add_node("legal_research", run_legal_research)
    g.add_node("consultant", run_consultant)
    g.add_node("prosecutor_r1", run_prosecutor_r1)
    g.add_node("defense_r1", run_defense_r1)
    g.add_node("prosecutor_r2", run_prosecutor_r2)
    g.add_node("defense_r2", run_defense_r2)
    g.add_node("judge", run_judge)
    g.add_node("reporter", run_reporter)
    g.add_node("top_consultant", run_top_consultant)

    # Set up the workflow sequence
    g.set_entry_point("case_manager")
    g.add_edge("case_manager", "legal_research")
    g.add_edge("legal_research", "consultant")
    g.add_edge("consultant", "prosecutor_r1")
    g.add_edge("prosecutor_r1", "defense_r1")
    g.add_edge("defense_r1", "prosecutor_r2")
    g.add_edge("prosecutor_r2", "defense_r2")
    g.add_edge("defense_r2", "judge")
    g.add_edge("judge", "reporter")
    g.add_edge("reporter", "top_consultant")
    g.add_edge("top_consultant", END)

    return g.compile()


# Singleton instance - import this in UI to run cases
court_graph = build_graph()
