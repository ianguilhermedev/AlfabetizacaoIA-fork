import os
import requests
from dotenv import load_dotenv
from google import genai
from loguru import logger
from alfabot.services.rag_service import buscar_contexto

# Carrega o arquivo .env IMEDIATAMENTE ao iniciar o módulo
load_dotenv()

# Configurações globais
PROVIDER = os.getenv("IA_PROVIDER", "ollama")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3.2")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# Inicialização do Cliente Gemini
client = None
if PROVIDER == "gemini":
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        client = genai.Client(api_key=api_key)
        logger.info(f"Provedor configurado com sucesso: Gemini ({GEMINI_MODEL})")
    else:
        logger.error("GEMINI_API_KEY não encontrada no .env!")


def _gerar_com_ollama(prompt: str) -> str:
    url = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": False}
    response = requests.post(url, json=payload, timeout=120)
    response.raise_for_status()
    return response.json().get("response", "").strip()


def _gerar_com_gemini(prompt: str) -> str:
    if not client:
        raise ValueError("Cliente Gemini não inicializado. Verifique seu .env.")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return response.text.strip()


def gerar_resposta_ia(mensagem_usuario: str, nivel_pedagogico: str = "iniciante") -> str:
    """Gera resposta usando o provedor configurado no .env"""
    logger.info(f"Buscando contexto para: '{mensagem_usuario}'")
    contexto = buscar_contexto(mensagem_usuario)

    prompt = f"""Você é um professor amigável e paciente, ensinando um aluno de nível {nivel_pedagogico}.
Use o CONTEXTO abaixo para responder à pergunta do aluno. Se a resposta não estiver no contexto, seja honesto e diga que não tem essa informação, mas tente ajudar de forma educativa.

CONTEXTO:
{contexto}

PERGUNTA:
{mensagem_usuario}

RESPOSTA:"""

    try:
        if PROVIDER == "gemini":
            logger.info("Enviando requisição para Gemini...")
            return _gerar_com_gemini(prompt)
        else:
            logger.info("Enviando requisição para Ollama...")
            return _gerar_com_ollama(prompt)
    except Exception as e:
        logger.error(f"Erro ao comunicar com {PROVIDER}: {e}")
        return "Desculpe, estou com dificuldades para pensar agora. Pode tentar novamente?"