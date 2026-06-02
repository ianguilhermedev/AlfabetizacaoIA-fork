from __future__ import annotations

from alfabot.domain.enums import PedagogicalLevel


def build_onboarding_buttons() -> dict:
    return {
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {"text": "Antes de começar, escolha seu nível de leitura."},
            "action": {
                "buttons": [
                    {"type": "reply", "reply": {"id": PedagogicalLevel.INICIANTE.value, "title": "Iniciante"}},
                    {"type": "reply", "reply": {"id": PedagogicalLevel.BASICO.value, "title": "Básico"}},
                    {"type": "reply", "reply": {"id": PedagogicalLevel.INTERMEDIARIO.value, "title": "Intermediário"}},
                ]
            },
        },
    }


def build_welcome_message(level: PedagogicalLevel) -> str:
    return f"Perfeito. Seu nível foi definido como {level.value}. Vamos seguir juntos."


def build_retry_prompt() -> str:
    return "Não consegui entender seu áudio. Pode gravar novamente, por favor?"


def build_level_response(level: PedagogicalLevel, user_text: str, context_snippets: list[str] | None = None) -> str:
    context_snippets = context_snippets or []
    context_text = " ".join(context_snippets)
    return f"[{level.value}] {user_text.strip()} {context_text}".strip()
