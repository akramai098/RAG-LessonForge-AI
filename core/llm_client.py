
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=120000,
        retry_options=types.HttpRetryOptions(attempts=2)
    )
)


def generate_text(
    prompt: str,
    temperature: float = 0.3,
    max_output_tokens: int = 3000
) -> str:
    """Generate text using the configured Gemini model."""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens
        )
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response.")

    return response.text
