"""AI Agents module - specialized agents for legal case analysis."""
from .case_analyst import run_case_manager
from .legal_researcher import run_legal_research
from .prosecutor import run_prosecutor_r1, run_prosecutor_r2
from .defense import run_defense_r1, run_defense_r2
from .judge import run_judge
from .reporter import run_reporter
from .consultant import run_consultant
from .top_consultant import run_top_consultant

__all__ = [
    "run_case_manager",
    "run_legal_research",
    "run_prosecutor_r1",
    "run_prosecutor_r2",
    "run_defense_r1",
    "run_defense_r2",
    "run_judge",
    "run_reporter",
    "run_consultant",
    "run_top_consultant",
]
