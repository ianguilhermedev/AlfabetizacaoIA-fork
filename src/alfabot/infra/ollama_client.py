from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass
class OllamaClient:
    model_name: str
    base_url: str = "http://localhost:11434"

    def generate(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model_name, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")
