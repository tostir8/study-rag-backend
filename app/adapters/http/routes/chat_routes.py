from fastapi import APIRouter
from pydantic import BaseModel

from app.application.use_cases.ask_question_use_case import (
    AskQuestionUseCase,
)
from app.infrastructure.ai.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from app.infrastructure.ai.llm.groq_provider import GroqProvider
from app.infrastructure.ai.rag.prompt_builder import PromptBuilder
from app.infrastructure.ai.rag.retriever import Retriever
from app.infrastructure.database.repositories.study_room_repository import (
    StudyRoomRepository,
)
from app.infrastructure.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


class QuestionRequest(BaseModel):
    question: str


@router.post("/study-room/{study_room_id}/ask")
def ask_question(
    study_room_id: str,
    request: QuestionRequest,
):
    """
    Answers a question using only the documents
    belonging to the specified Study Room.
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

    prompt_builder = PromptBuilder()

    llm = GroqProvider()

    use_case = AskQuestionUseCase(
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    answer = use_case.execute(
        question=request.question,
        study_room_id=study_room_id,
    )

    return {
        "study_room_id": study_room_id,
        "question": request.question,
        "answer": answer,
    }
