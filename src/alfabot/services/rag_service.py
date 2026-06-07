import chromadb
import os

# Define onde o banco será salvo fisicamente no disco
DB_PATH = os.path.join("data", "chroma_db")
COLLECTION_NAME = "conhecimento_marajo"

# Inicializa o cliente do ChromaDB com persistência
# Isso garante que os dados não sumam ao fechar o bot
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)


def adicionar_conhecimento(texto: str, id_documento: str):
    """Adiciona um fato novo ao banco de dados."""
    collection.add(
        documents=[texto],
        ids=[id_documento]
    )


def buscar_contexto(pergunta: str, n_resultados: int = 2) -> str:
    """Busca os trechos mais relevantes no banco de dados."""
    resultados = collection.query(
        query_texts=[pergunta],
        n_results=n_resultados
    )

    # Extrai apenas os documentos encontrados (pode haver mais de um)
    documentos = resultados.get('documents', [[]])[0]

    # Junta tudo em um único texto para enviar à IA
    return "\n".join(documentos)