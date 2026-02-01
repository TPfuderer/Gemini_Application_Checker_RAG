"""
Gemini LLM client using the official google-genai SDK.

Design:
- Gemini is used ONLY for generation (RAG stays model-agnostic).
- Primary model optimized for instruction-following and RAG synthesis.
- Fallback model used when free-tier limits or availability issues occur.
"""

import os
from google import genai
from google.genai.errors import ClientError


def get_client():
    """
    Initialize and return a Gemini client.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY (or GEMINI_API_KEY) environment variable not set."
        )

    return genai.Client(api_key=api_key)


# -------------------------------------------------
# Model selection
# -------------------------------------------------
PRIMARY_MODEL = "models/gemini-2.5-flash-lite"
FALLBACK_MODEL = "models/gemma-3-4b-it"


def generate_answer(client, context: str, question: str, system_prompt: str):
    prompt = f"""{system_prompt}

Context:
{context}

Question:
{question}
"""

    try:
        response = client.models.generate_content(
            model=PRIMARY_MODEL,
            contents=prompt,
            config={
                "temperature": 0.1,
                "max_output_tokens": 600,
            },
        )
        return response.text.strip(), "Gemini Flash (primary)"

    except ClientError:
        # Graceful fallback on quota / availability issues
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 600,
            },
        )
        return response.text.strip(), "Gemma 3B (fallback – free tier limit)"
