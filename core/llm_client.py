import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()
API_KEY = os.getenv("CEREBRAS_API_KEY")
MODEL = os.getenv("CEREBRAS_MODEL")

client = Cerebras(api_key=API_KEY)

def call_llm(prompt: str, temperature: float = 0.7) -> str:
    """Call Cerebras API with streaming and return full content."""
    try:
        stream = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=MODEL,
            stream=True,
            max_completion_tokens=2000,
            temperature=temperature,
        )
        output = ""
        for chunk in stream:
            output += chunk.choices[0].delta.content or ""
        return output
    except Exception as e:
        return f"[LLM Error] {e}"
