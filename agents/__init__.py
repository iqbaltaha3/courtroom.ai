import os
import json
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from typing import Type, TypeVar

# Load environment variables from .env file
load_dotenv()

# Fast, lightweight model for prose output (call_claude)
MODEL_PROSE = "llama-3.1-8b-instant"
# Model for structured output with simple schemas (no nested models)
MODEL_SIMPLE_STRUCT = "openai/gpt-oss-20b"
# Model for structured output with complex nested schemas
MODEL_COMPLEX_STRUCT = "openai/gpt-oss-120b"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

T = TypeVar("T", bound=BaseModel)


def call_claude(system: str, user: str) -> str:
    """Plain-text call for prose output.
    Uses lightweight model for speed and token efficiency.
    For agents: prosecutor, defense, reporter, consultant."""
    response = client.chat.completions.create(
        model=MODEL_PROSE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    )
    return response.choices[0].message.content.strip()


def call_structured(system: str, user: str, schema: Type[T], retries: int = 1, use_complex_model: bool = False) -> T:
    """Structured call using json_schema for strict schema enforcement.
    
    Automatically selects model based on schema complexity:
    - SIMPLE_STRUCT (openai/gpt-oss-20b) for simple schemas without nested models
    - COMPLEX_STRUCT (openai/gpt-oss-120b) for schemas with nested Pydantic models ($defs)
    - Override with use_complex_model=True to force COMPLEX_STRUCT
    
    Retries once on validation failure before propagating the error.
    """
    # Extract the JSON schema from the Pydantic model
    pydantic_schema = schema.model_json_schema()
    has_nested_schemas = "$defs" in pydantic_schema
    
    # Select model based on schema complexity or explicit flag
    model = MODEL_COMPLEX_STRUCT if (use_complex_model or has_nested_schemas) else MODEL_SIMPLE_STRUCT
    
    # Build the full schema including nested model definitions
    full_schema = {
        "type": "object",
        "properties": pydantic_schema.get("properties", {}),
        "required": pydantic_schema.get("required", []),
        "additionalProperties": False
    }
    
    # Include $defs if present (for nested models like ApplicableSection, Precedent)
    if "$defs" in pydantic_schema:
        full_schema["$defs"] = pydantic_schema["$defs"]
    
    last_error = None
    for attempt in range(retries + 1):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": schema.__name__,
                        "schema": full_schema
                    }
                },
                temperature=0.0,
            )
            
            return schema.model_validate_json(response.choices[0].message.content)
        except Exception as e:
            last_error = e
    
    raise last_error