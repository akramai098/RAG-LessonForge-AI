from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=120000,
        retry_options=types.HttpRetryOptions(attempts=1)
    )
)

try:
    print("Testing model:", GEMINI_MODEL)
    print("Waiting for Gemini response...")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Say hello.",
        config=types.GenerateContentConfig(
            max_output_tokens=20,
            temperature=0
        )
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nERROR:", type(e).__name__)
    print(e)

finally:
    client.close()