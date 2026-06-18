import ollama

MODEL = "gemma3:12b"

def call_claude(system: str, user: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return response["message"]["content"].strip()
