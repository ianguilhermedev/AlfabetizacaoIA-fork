import os
import chromadb
from src.alfabot.logger_config import logger

# Configurações
DB_PATH = os.path.join("data", "chroma_db")
COLLECTION_NAME = "conhecimento_marajo"

# Variáveis privadas para a inicialização lazy
_client = None
_collection = None


def _get_collection():
    """Inicializa o cliente e a coleção do ChromaDB apenas sob demanda."""
    global _client, _collection

    if _collection is None:
        # Garante que o diretório de dados exista
        os.makedirs(DB_PATH, exist_ok=True)

        # Inicializa com persistência
        _client = chromadb.PersistentClient(path=DB_PATH)
        _collection = _client.get_or_create_collection(name=COLLECTION_NAME)
        logger.info(f"Conexão com ChromaDB estabelecida em {DB_PATH}")

    return _collection


def adicionar_conhecimento(texto: str, id_documento: str):
    """Adiciona um fato novo ao banco de dados."""
    try:
        collection = _get_collection()
        collection.add(
            documents=[texto],
            ids=[id_documento]
        )
        logger.info(f"Conhecimento adicionado com sucesso (ID: {id_documento})")
    except Exception as e:
        logger.error(f"Erro ao adicionar conhecimento ao ChromaDB: {e}")


def buscar_contexto(pergunta: str, n_resultados: int = 2) -> str:
    """Busca os trechos mais relevantes no banco de dados."""
    try:
        collection = _get_collection()
        resultados = collection.query(
            query_texts=[pergunta],
            n_results=n_resultados
        )

        # Extrai apenas os documentos encontrados
        documentos = resultados.get('documents', [[]])[0]

        contexto = "\n".join(documentos)
        logger.info(
            f"Contexto recuperado para pergunta '{pergunta[:20]}...': {len(documentos)} resultados encontrados.")

        return contexto
    except Exception as e:
        logger.error(f"Erro ao buscar contexto no ChromaDB: {e}")
        return ""