from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection

from app.application.ports.vector_store_port import VectorStorePort
from app.config.settings import get_settings


class ChromaVectorStore(VectorStorePort):
    """
    ChromaDB implementation of the VectorStorePort.

    Responsible for storing and retrieving document
    embeddings from the vector database.
    """

    def __init__(self) -> None:
        settings = get_settings()

        self._client = chromadb.HttpClient(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
        )

        self._collection: Collection = (
            self._client.get_or_create_collection(
                name="study_rag_documents",
            )
        )

    def add(
        self,
        document_id: str,
        embeddings: list[list[float]],
        documents: list[str],
        metadata: list[dict[str, Any]],
    ) -> None:
        """
        Stores document embeddings inside ChromaDB.
        """

        ids = [
            f"{document_id}_{index}"
            for index in range(len(documents))
        ]

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadata,
        )

    def search(
        self,
        embedding: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Searches the most relevant chunks.
        """

        results = self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            where=filters,
        )

        return [
            {
                "document": document,
                "metadata": metadata,
                "distance": distance,
            }
            for document, metadata, distance in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

    def delete_document(
        self,
        document_id: str,
    ) -> None:
        """
        Deletes every chunk associated with a document.
        """

        self._collection.delete(
            where={
                "document_id": document_id,
            }
        )
