from fastapi import APIRouter
from pydantic import BaseModel

from app.application.use_cases.generate_exam_use_case import (
    GenerateExamUseCase,
)
from app.infrastructure.ai.embeddings.sentence_transformer_provider import (
    SentenceTransformerEmbeddingProvider,
)
from app.infrastructure.ai.llm.groq_provider import GroqProvider
from app.infrastructure.ai.prompts.exam_prompt_builder import (
    ExamPromptBuilder,
)
from app.infrastructure.ai.rag.retriever import Retriever
from app.infrastructure.database.repositories.study_room_repository import (
    StudyRoomRepository,
)
from app.infrastructure.vector_store.chroma_vector_store import (
    ChromaVectorStore,
)

router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
)


class ExamRequest(BaseModel):
    multiple_choice: int = 5
    true_false: int = 3
    open_questions: int = 2


@router.post("/study-room/{study_room_id}")
def generate_exam(
    study_room_id: str,
    request: ExamRequest,
):
    """
    Generates an academic exam using only the
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

    prompt_builder = ExamPromptBuilder()

    llm = GroqProvider()

    use_case = GenerateExamUseCase(
        retriever=retriever,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    exam = use_case.execute(
        study_room_id=study_room_id,
        multiple_choice=request.multiple_choice,
        true_false=request.true_false,
        open_questions=request.open_questions,
    )

    return {
        "study_room_id": study_room_id,
        **exam,
    }
