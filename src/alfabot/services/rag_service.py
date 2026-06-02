from __future__ import annotations


class RagService:
    def __init__(self, chroma_service):
        self.chroma_service = chroma_service

    def buscar_contexto(self, query: str, top_k: int = 3) -> list[str]:
        return self.chroma_service.buscar_contexto(query, top_k=top_k)
