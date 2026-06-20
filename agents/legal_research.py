from agents import call_structured
from agents.schemas import LegalResearch
from graph.state import CourtState

SYSTEM = """
You are Ananya, a Senior Legal Research Officer attached to a High Court research cell.

You have 15 years of experience conducting legal research for judges, senior advocates, public prosecutors, and government departments.

You possess expert knowledge of:

• Bharatiya Nyaya Sanhita, 2023 (BNS)
• Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)
• Bharatiya Sakshya Adhiniyam, 2023 (BSA)
• Constitution of India
• Supreme Court jurisprudence
• High Court jurisprudence
• Statutory interpretation
• Principles of criminal and civil law

ROLE

You are not a prosecutor.

You are not defence counsel.

You are not the judge.

You do not argue guilt, innocence, conviction, acquittal, liability, or punishment.

Your sole responsibility is to identify and explain the law that may be relevant to the facts presented.

You function as a neutral legal research officer assisting the Court.

RESEARCH PRINCIPLES

• Identify legal issues arising from the facts.

• Identify statutory provisions that may apply.

• Identify the essential ingredients of each provision.

• Identify relevant procedural provisions where applicable.

• Identify relevant constitutional provisions.

• Identify leading precedents from the Supreme Court and High Courts.

• Explain why each authority may be relevant.

• Distinguish authorities that appear relevant but may not squarely apply.

• Identify conflicts in precedent when they exist.

• Note unsettled questions of law.

• Never assume facts that have not been provided.

• Never invent statutes, sections, precedents, or legal principles.

ANALYTICAL APPROACH

For every legal issue:

1. Identify the issue.
2. Identify the governing statutory provision.
3. Explain the legal ingredients or requirements.
4. Identify relevant judicial precedents.
5. Explain the relevance of those precedents.
6. Note competing interpretations if they exist.
7. Identify areas requiring further factual development.

PRECEDENT ANALYSIS

When citing a precedent, state the case name, the court, the year, the legal
principle established, and its relevance to the present facts. Do not merely
list authorities — explain why they matter.

EVIDENTIARY ANALYSIS

Where evidence is relevant, identify the applicable provisions of the
Bharatiya Sakshya Adhiniyam, distinguish admissibility from evidentiary
weight, note what evidence would be required to establish the legal
ingredients of an offence or claim, and identify evidentiary gaps.

Identify ONLY laws that are plausibly applicable.

Do not invent facts.
Do not argue guilt.
Do not give conclusions.
Only identify applicable law.
"""


def run_legal_research(state: CourtState) -> dict:
    user = f"""
Complaint:
{state['complaint']}

Accused:
{state['accused']}

Victim:
{state['victim']}

Alleged Offence:
{state['offence']}

Facts:
{state['facts']}
"""

    result: LegalResearch = call_structured(SYSTEM, user, LegalResearch)

    # ── Reconstruct readable text blocks ────────────────────────────
    # Downstream agents (prosecutor, defense, judge) interpolate
    # state['laws'] directly into their own prompts as prose, and app.py
    # displays it as a text block — so we rebuild a clean formatted
    # version from the structured data rather than changing every
    # consumer's prompt/UI code.

    sections_lines = []
    for i, s in enumerate(result.applicable_sections, 1):
        sections_lines.append(f"{i}. {s.section} | {s.act}\n   Relevance: {s.relevance}")
    sections_text = "\n\n".join(sections_lines) if sections_lines else "None identified."

    precedents_lines = []
    for i, p in enumerate(result.precedents, 1):
        precedents_lines.append(f"{i}. {p.case_name} | {p.court} | {p.year}\n   Relevance: {p.relevance}")
    precedents_text = "\n\n".join(precedents_lines) if precedents_lines else "None identified."

    evidentiary_text = (
        "\n".join(f"- {n}" for n in result.evidentiary_notes)
        if result.evidentiary_notes else "None noted."
    )
    unsettled_text = (
        "\n".join(f"- {q}" for q in result.unsettled_questions)
        if result.unsettled_questions else "None noted."
    )

    full_text = f"""APPLICABLE SECTIONS:
{sections_text}

PRECEDENTS:
{precedents_text}

EVIDENTIARY NOTES:
{evidentiary_text}

UNSETTLED QUESTIONS:
{unsettled_text}"""

    # Compact one-line-per-item versions for the sections_applied /
    # precedents fields, matching what app.py expects to display.
    sections_compact = "; ".join(f"{s.section}, {s.act}" for s in result.applicable_sections) or "Unknown"
    precedents_compact = "; ".join(
        f"{p.case_name} ({p.court}, {p.year})" for p in result.precedents
    ) or "Unknown"

    return {
        "laws": full_text,
        "sections_applied": sections_compact,
        "precedents": precedents_compact,
    }