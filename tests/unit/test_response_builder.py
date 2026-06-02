from __future__ import annotations

from alfabot.domain.enums import PedagogicalLevel
from alfabot.prompts.system_prompt import build_system_prompt
from alfabot.services.response_builder import build_level_response


def test_build_level_response_includes_level_and_context():
    result = build_level_response(
        PedagogicalLevel.INICIANTE,
        "O que é um búfalo?",
        ["Búfalo é um símbolo importante do Marajó."],
    )

    assert "[iniciante]" in result
    assert "búfalo" in result.lower()


def test_build_system_prompt_injects_level_and_marajoara_context():
    prompt = build_system_prompt("básico", ["Cerâmica marajoara é um patrimônio cultural."])

    assert "Nível atual: básico" in prompt
    assert "Cerâmica marajoara" in prompt
