from typing import Any

from app.application.ports.embedding_port import EmbeddingPort
from app.application.ports.vector_store_port import VectorStorePort


class Retriever:
    """
    Retrieves the most relevant document chunks
    for a user question inside a Study Room.
    """

    def __init__(
        self,
        embedding_provider: EmbeddingPort,
        vector_store: VectorStorePort,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def retrieve(
        self,
        question: str,
        study_room_id: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Retrieves the most relevant chunks
        from a single Study Room.
        """

        embedding = self._embedding_provider.embed(
            question,
        )

        return self._vector_store.search(
            embedding=embedding,
            top_k=top_k,
            filters={
                "study_room_id": study_room_id,
            },
        )
