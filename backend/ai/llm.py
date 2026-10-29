from backend.app.config import settings
import requests

class LLM:
    def __init__(self):
        self.model = settings.LLM_MODEL
        self.url = settings.OLLAMA_URL

    def generate(self, prompt: str):
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            data = response.json()

            # Ollama returns { "response": "text..." }
            return data.get("response", "")

        except Exception as e:
            print("LLM error:", e)
            return "⚠️ LLM backend error."

# THIS is what orchestrator imports
llm = LLM()
