import requests

from app.config import OLLAMA_HOST, OLLAMA_MODEL


class LLMClient:
    def chat(self, messages):
        response = requests.post(
            f"{OLLAMA_HOST}/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": messages,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["message"]["content"]
