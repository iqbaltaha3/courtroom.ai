"""LLM Service - handles communication with Groq API for case analysis."""
import os
import time
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from typing import Type, TypeVar

# Load environment variables
load_dotenv()

# Try to load from Streamlit secrets (for hosted deployments)
try:
    import streamlit as st
    GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except (ImportError, AttributeError, FileNotFoundError):
    # Fallback to environment variables (local development)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ========== LLM MODELS ==========
MODEL_PROSE = "llama-3.1-8b-instant"           # Fast prose generation
MODEL_SIMPLE_STRUCT = "openai/gpt-oss-20b"     # Structured output (simple schemas)
MODEL_COMPLEX_STRUCT = "openai/gpt-oss-120b"   # Structured output (complex schemas)

# Initialize Groq client with API key from Streamlit secrets or environment
client = Groq(api_key=GROQ_API_KEY)

T = TypeVar("T", bound=BaseModel)


def call_claude(system: str, user: str, max_tokens: int = 1000) -> str:
    """Call LLM for prose/narrative output.
    
    Args:
        system: System prompt defining agent behavior
        user: User message/question
        max_tokens: Maximum output length (default 1000)
    
    Returns:
        Plain text response from LLM
    
    Used by: Prosecutor, Defense, Reporter, Consultant agents
    """
    response = client.chat.completions.create(
        model=MODEL_PROSE,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def call_structured(
    system: str,
    user: str,
    schema: Type[T],
    retries: int = 3,
    use_complex_model: bool = False,
    max_tokens: int = 2000
) -> T:
    """Call LLM for structured JSON output with schema validation.
    
    Args:
        system: System prompt defining agent behavior
        user: User message/question
        schema: Pydantic model for output schema
        retries: Number of retry attempts on rate limit (default 3)
        use_complex_model: Force use of complex model (default False - auto-detect)
        max_tokens: Maximum output length (default 2000)
    
    Returns:
        Validated Pydantic model instance
    
    Used by: Case Manager, Legal Researcher, Judge agents
    
    Features:
    - Auto-detects schema complexity and selects appropriate model
    - Handles rate limiting with exponential backoff
    - Strict schema validation with json_schema
    """
    # Extract JSON schema from Pydantic model
    pydantic_schema = schema.model_json_schema()
    has_nested_schemas = "$defs" in pydantic_schema
    
    # Auto-select model based on complexity
    model = (
        MODEL_COMPLEX_STRUCT
        if (use_complex_model or has_nested_schemas)
        else MODEL_SIMPLE_STRUCT
    )
    
    # Build full schema including nested definitions
    full_schema = {
        "type": "object",
        "properties": pydantic_schema.get("properties", {}),
        "required": pydantic_schema.get("required", []),
        "additionalProperties": False,
    }
    
    if "$defs" in pydantic_schema:
        full_schema["$defs"] = pydantic_schema["$defs"]
    
    last_error = None
    for attempt in range(retries):
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
                        "schema": full_schema,
                    },
                },
                temperature=0.0,
                max_tokens=max_tokens,
            )
            
            return schema.model_validate_json(response.choices[0].message.content)
        
        except Exception as e:
            last_error = e
            error_code = getattr(e, "code", None)
            
            # Retry on rate limit with exponential backoff
            if error_code == "rate_limit_exceeded" and attempt < retries - 1:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(
                    f"[RATE_LIMIT] Attempt {attempt + 1}/{retries} failed, "
                    f"waiting {wait_time}s..."
                )
                time.sleep(wait_time)
                continue
            
            break
    
    raise last_error
