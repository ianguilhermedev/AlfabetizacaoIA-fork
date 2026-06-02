from __future__ import annotations

from alfabot.domain.enums import PedagogicalLevel
from alfabot.prompts.system_prompt import build_system_prompt
from alfabot.services.response_builder import build_level_response


class AIService:
    def __init__(self, ollama_client):
        self.ollama_client = ollama_client

    def generate_reply(self, level: PedagogicalLevel, user_text: str, context_snippets: list[str] | None = None) -> str:
        context_snippets = context_snippets or []
        prompt = build_system_prompt(level.value, context_snippets)
        prompt = f"{prompt}\n\nPergunta do aluno: {user_text}"
        reply = self.ollama_client.generate(prompt)
        if reply:
            return reply.strip()
        return build_level_response(level, user_text, context_snippets)
