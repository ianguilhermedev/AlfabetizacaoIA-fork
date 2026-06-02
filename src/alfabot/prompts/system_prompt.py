from __future__ import annotations


def build_system_prompt(level: str, context_snippets: list[str] | None = None) -> str:
    context_snippets = context_snippets or []
    context_text = "\n".join(f"- {snippet}" for snippet in context_snippets)
    return (
        "Você é um assistente pedagógico acolhedor para alfabetização. "
        f"Nível atual: {level}.\n"
        "Use linguagem gentil, simples e contextualizada com a cultura marajoara.\n"
        f"Contexto cultural:\n{context_text}"
    ).strip()
