"""
Gemini LLM client using the official google-genai SDK (future-proof).

Design:
- Uses the unified GenAI Client (text, multimodal, tools-ready).
- Gemini is used ONLY for generation (RAG stays model-agnostic).
- Low temperature for stable, non-hallucinated answers.
"""

import os
from google import genai
from rag.prompts import SYSTEM_PROMPT_ALL, SYSTEM_PROMPT_PROJECT



def get_client():
    """
    Initialize and return a Gemini client.
    """
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY (or GEMINI_API_KEY) environment variable not set."
        )

    client = genai.Client(api_key=api_key)
    return client


from google.genai.errors import ClientError

PRIMARY_MODEL = "models/gemma-3-4b-it"
FALLBACK_MODEL = "models/gemini-2.5-flash-lite"


def generate_answer(client, context: str, question: str, system_prompt: str):
    prompt = f"""
    {system_prompt}

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
                "max_output_tokens": 512,
            },
        )
        return response.text.strip(), PRIMARY_MODEL

    except ClientError:
        # Fallback on quota / availability issues
        response = client.models.generate_content(
            model=FALLBACK_MODEL,
            contents=prompt,
            config={
                "temperature": 0.2,
                "max_output_tokens": 512,
            },
        )
        return response.text.strip(), FALLBACK_MODEL


