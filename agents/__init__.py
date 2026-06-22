import ollama
from pydantic import BaseModel
from typing import Type, TypeVar

MODEL = "qwen3:8b"

T = TypeVar("T", bound=BaseModel)


def call_claude(system: str, user: str) -> str:
    """Plain-text call. Kept for agents that don't need structured output
    (case manager, legal research, reporter — anything that's prose/free-form)."""
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return response["message"]["content"].strip()


def call_structured(system: str, user: str, schema: Type[T], retries: int = 1) -> T:
    """Structured call. Pass a Pydantic model class as `schema`; Ollama
    constrains generation to that JSON schema, and we parse + validate
    the result through Pydantic before returning it.

    `format=` constrains the model's token generation to valid JSON
    matching the schema's shape (types, required fields), but it does NOT
    guarantee semantic constraints like Literal enums or numeric ge/le
    bounds — the model can still emit a value outside an int range or a
    string not in a Literal's allowed set. We retry once on validation
    failure (asking again often fixes it) before propagating the error,
    since a transient bad generation shouldn't crash the whole graph run.
    """
    last_error = None
    for attempt in range(retries + 1):
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            format=schema.model_json_schema(),
        )
        try:
            return schema.model_validate_json(response["message"]["content"])
        except Exception as e:  # pydantic.ValidationError or malformed JSON
            last_error = e
    raise last_error