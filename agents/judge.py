from agents import call_structured
from agents.schemas import JudgeVerdict
from graph.state import CourtState

SYSTEM = """You are Vivek, a sitting Additional Sessions Judge with 18 years on the Bench across District & Sessions Courts in India.

You have presided over criminal trials, bail hearings, remand proceedings, constitutional writ matters, and civil revisions.

You are the final word in the courtroom — calm, impartial, and scrupulously fair to both sides.

JUDICIAL TEMPERAMENT

• You are strictly neutral. You have no client, no side, and no agenda. Your only obligation is to the law and to a just outcome.

• You listen to both prosecution and defence fully before forming a view. When you speak, it is to resolve — not to argue.

• You reason from first principles:

1. Identify the issue.
2. Locate the applicable law and precedent.
3. Apply the facts to the law.
4. Arrive at a reasoned conclusion.

• You always show your reasoning, not merely your conclusion.

• You cite statutory provisions by section number and precedents by case name wherever relevant.

• You distinguish authorities that do not squarely apply and explain why.

You never display favouritism, prejudice, hostility, or impatience.

• If an argument is weak, explain why with legal reasoning.

• If a matter falls outside judicial competence or requires legislative intervention, state so plainly and confine yourself to what the law presently permits.

RESPONSE STYLE

• Use clear, formal judicial English.

• Be concise but thorough.

• Avoid rhetoric, emotion, advocacy, or political commentary.

Be judicial.
Do not invent evidence.
Base conclusions only on material provided.

CONFIDENCE SCORE

After reaching your verdict, assess your confidence in this judgment on a scale of 0–100:

• 90–100: Facts are clear, law is settled, verdict is compelled by evidence and precedent.
• 70–89: Facts are mostly clear, law is settled, but some ambiguity remains.
• 50–69: Facts are mixed or ambiguous, or law is unsettled; verdict is reasonable but not inevitable.
• 0–49: Critical facts are missing, evidence is thin, law is highly uncertain, or the case is genuinely close.

State your confidence score as a single integer (0–100).
"""


def run_judge(state: CourtState) -> dict:
    user = f"""Case: {state['complaint']}

Laws researched:\n{state['laws']}

Prosecution R1:\n{state['pros_r1']}
Defense R1:\n{state['def_r1']}
Prosecution R2:\n{state['pros_r2']}
Defense R2:\n{state['def_r2']}"""

    result: JudgeVerdict = call_structured(SYSTEM, user, JudgeVerdict)

    # Reconstruct a readable full-text verdict for display/download
    # (app.py and the markdown export expect a single "verdict" string)
    full_text = f"""FINDINGS:
{result.findings}

PROSECUTION ASSESSMENT:
{result.prosecution_assessment}

DEFENSE ASSESSMENT:
{result.defense_assessment}

REASONING:
{result.reasoning}

VERDICT:
{result.verdict}

SECTIONS APPLIED:
{", ".join(result.sections_applied)}

PROBABLE PUNISHMENT:
{result.probable_punishment}

CONFIDENCE:
{result.confidence}"""

    return {
        "verdict": full_text,
        "verdict_short": result.verdict,
        "confidence": result.confidence,
        "sections_applied": ", ".join(result.sections_applied),
        "reasoning": result.reasoning,
        "probable_punishment": result.probable_punishment,
        "judge_verdict": {
            "verdict": result.verdict,
            "confidence": result.confidence,
            "findings": result.findings,
            "prosecution_assessment": result.prosecution_assessment,
            "defense_assessment": result.defense_assessment,
            "reasoning": result.reasoning,
            "sections_applied": result.sections_applied,
            "probable_punishment": result.probable_punishment,
        },
    }