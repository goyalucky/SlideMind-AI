import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

class Summarizer:
    def __init__(self, model: str = "gemini-3.5-flash-lite"):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing from your .env file")
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.model = model

    def summarize_text(self, text: str, max_retries: int = 3) -> str:
        prompt = (
            "Summarize the following text into clear bullet points suitable "
            "for a PowerPoint presentation slide:\n\n"
            f"{text}"
        )

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    # Explicit config avoids automatic function calling (AFC) warnings
                    config=types.GenerateContentConfig(
                        temperature=0.3,
                    )
                )
                if response.text:
                    return response.text

            except errors.APIError as e:
                err_msg = str(e)
                print(f"[{self.model}] API Notice: {err_msg[:120]}...")

                if "429" in err_msg or "RESOURCE_EXHAUSTED" in err_msg or "503" in err_msg:
                    wait_time = 10 * (attempt + 1)
                    print(f"Server busy or rate limited. Retrying in {wait_time}s ({attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    raise e
            except Exception as e:
                raise e

        raise RuntimeError("Quota or capacity limit reached. Please retry in a few moments.")

if __name__ == "__main__":
    sample_text = (
        "Artificial intelligence is changing the way people work and learn. "
        "Many companies are using AI tools to automate repetitive tasks, analyze "
        "large amounts of data, and provide better services to their customers."
    )

    summarizer = Summarizer()
    summary = summarizer.summarize_text(sample_text)
    print("\n**Summarized Text:**\n")
    print(summary)