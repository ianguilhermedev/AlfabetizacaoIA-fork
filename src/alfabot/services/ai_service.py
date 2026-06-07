import os
import requests
from loguru import logger
from alfabot.services.rag_service import buscar_contexto

# Carrega as variáveis do .env (ajustadas para os nomes que você forneceu)
OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")  # Usando OLLAMA_MODEL como no seu .env


def gerar_resposta_ia(mensagem_usuario: str, nivel_pedagogico: str = "iniciante") -> str:
    """
    Gera uma resposta usando o modelo local, incorporando o contexto do RAG.
    """
    logger.info(f"Buscando contexto no banco para: '{mensagem_usuario}'")

    # 1. Busca o conhecimento no ChromaDB
    contexto = buscar_contexto(mensagem_usuario)

    # 2. Monta o Prompt de Sistema
    prompt = f"""Você é um professor amigável e paciente, ensinando um aluno de nível {nivel_pedagogico}.
Use o CONTEXTO abaixo para responder à pergunta do aluno. 
Se a resposta não estiver no contexto, seja honesto e diga que não tem essa informação, mas tente ajudar de forma educativa.
Responda de forma clara e em português.

CONTEXTO:
{contexto}

PERGUNTA DO ALUNO:
{mensagem_usuario}

RESPOSTA:"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=999)
        response.raise_for_status()
        resultado = response.json()
        return resultado.get("response", "").strip()

    except Exception as e:
        logger.error(f"Erro ao comunicar com o Ollama: {e}")
        return "Desculpe, estou com dificuldades para pensar agora. Pode tentar novamente?"