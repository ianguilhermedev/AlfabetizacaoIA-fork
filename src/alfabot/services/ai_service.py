import ollama

def gerar_resposta_ia(texto_aluno: str, nivel: str) -> str:
    # Prompt de sistema que define o comportamento pedagógico
    system_prompt = (
        f"Você é um tutor pedagógico do Alfabot Marajoara. "
        f"Responda de forma simples, encorajadora e use elementos da cultura marajoara. "
        f"O nível do aluno é: {nivel}."
    )

    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': texto_aluno},
    ])

    return response['message']['content']