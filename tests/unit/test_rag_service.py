from __future__ import annotations

from alfabot.infra.chroma import ChromaService
from alfabot.services.rag_service import RagService


def test_buscar_contexto_returns_relevant_marajoara_snippet():
    chroma = ChromaService("./tmp/chroma")
    chroma.add_document("Búfalo do Marajó", "O búfalo do Marajó vive em áreas alagadas e faz parte do cotidiano local.")
    chroma.add_document("Cerâmica marajoara", "A cerâmica marajoara destaca traços culturais e artísticos.")

    service = RagService(chroma)
    results = service.buscar_contexto("Quero aprender sobre búfalo")

    assert results
    assert "búfalo" in results[0].lower()
