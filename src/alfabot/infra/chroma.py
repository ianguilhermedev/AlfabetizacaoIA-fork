from __future__ import annotations


class ChromaService:
    def __init__(self, path: str):
        self.path = path
        self._documents: list[dict[str, str]] = []

    def buscar_contexto(self, query: str, top_k: int = 3) -> list[str]:
        query_terms = {term for term in query.lower().split() if len(term) > 2}

        scored_documents: list[tuple[int, str]] = []
        for document in self._documents:
            content = document["chunk_text"]
            content_terms = {term for term in content.lower().split() if len(term) > 2}
            score = len(query_terms & content_terms)
            if score > 0:
                scored_documents.append((score, content))

        scored_documents.sort(key=lambda item: item[0], reverse=True)
        return [content for _score, content in scored_documents[:top_k]]

    def add_document(self, source_title: str, chunk_text: str, topic_tags: str | None = None, language: str | None = None) -> None:
        self._documents.append(
            {
                "source_title": source_title,
                "chunk_text": chunk_text,
                "topic_tags": topic_tags or "",
                "language": language or "pt-BR",
            }
        )
