from typing import TypedDict, Optional


class CourtState(TypedDict):
    # ── Input ──────────────────────────────────────────
    complaint: str

    # ── Agent 1: Case Manager ──────────────────────────
    entities: Optional[str]        # accused, victim, offence, key facts
    accused: Optional[str]
    offence: Optional[str]
    victim: Optional[str]
    facts: Optional[str]

    # ── Agent 2: Legal Research ────────────────────────
    laws: Optional[str]
    sections_applied: Optional[str]
    precedents: Optional[str]           # applicable sections + precedents

    # ── Agent 3 & 4: Round 1 ──────────────────────────
    pros_r1: Optional[str]
    def_r1: Optional[str]

    # ── Agent 3 & 4: Round 2 ──────────────────────────
    pros_r2: Optional[str]
    def_r2: Optional[str]

    # ── Agent 5: Judge ─────────────────────────────────
    verdict: Optional[str]         # full verdict text
    verdict_short: Optional[str]   # Guilty / Not Guilty / Partial
    confidence: Optional[int]      # 0-100
    sections_applied: Optional[str]
    probable_punishment: Optional[str]

    # ── Agent 6: Reporter ──────────────────────────────
    headline: Optional[str]
    report: Optional[str]          # journalistic summary
