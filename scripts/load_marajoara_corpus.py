from __future__ import annotations

from alfabot.infra.chroma import ChromaService


def load_default_corpus(chroma_service: ChromaService) -> None:
    chroma_service.add_document(
        "Cerâmica marajoara",
        "A cerâmica marajoara é conhecida por seus desenhos geométricos e forte valor cultural.",
        topic_tags="cultura,ceramica",
    )
    chroma_service.add_document(
        "Búfalo do Marajó",
        "O búfalo do Marajó aparece no cotidiano local e pode ser usado como contexto de leitura.",
        topic_tags="fauna,bufalo",
    )
    chroma_service.add_document(
        "Lendas do Marajó",
        "As lendas do Marajó ajudam a aproximar a leitura do imaginário e da identidade local.",
        topic_tags="lenda,tradicao",
    )


if __name__ == "__main__":
    load_default_corpus(ChromaService("./data/chroma"))
