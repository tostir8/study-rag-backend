from fastapi import APIRouter
from pydantic import BaseModel

from app.application.use_cases.generate_flashcards_use_case import (
    GenerateFlashcardsUseCase,
)
from app.infrastructure.ai.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from app.infrastructure.ai.llm.groq_provider import GroqProvider
from app.infrastructure.ai.prompts.flashcard_prompt_builder import (
    FlashcardPromptBuilder,
)
from app.infrastructure.ai.rag.retriever import Retriever
from app.infrastructure.database.repositories.study_room_repository import (
    StudyRoomRepository,
)
from app.infrastructure.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

router = APIRouter(
    prefix="/flashcards",
    tags=["Flashcards"],
)


class FlashcardRequest(BaseModel):
    amount: int = 10


@router.post("/study-room/{study_room_id}")
def generate_flashcards(
    study_room_id: str,
    request: FlashcardRequest,
):
    """
    Generates study flashcards using only the
    documents contained in a Study Room.
    """

    room = StudyRoomRepository().get_by_id(
        study_room_id,
    )

    if room is None:
        return {
            "message": "Study Room not found.",
        }

    vector_store = ChromaVectorStore()

    embedding_provider = (
        SentenceTransformerEmbeddingProvider()
    )

    retriever = Retriever(
        embedding_provider=embedding_provider,
        vector_store=vector_store,
    )

    prompt_builder = FlashcardPromptBuilder()

    llm = GroqProvider()

    use_case = GenerateFlashcardsUseCase(
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    flashcards = use_case.execute(
        study_room_id=study_room_id,
        amount=request.amount,
    )

    return {
        "study_room_id": study_room_id,
        **flashcards,
    }
