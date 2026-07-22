from app.application.ports.llm_port import LLMPort
from app.infrastructure.ai.prompts.chat_prompt_builder import (
    ChatPromptBuilder,
)
from app.infrastructure.ai.rag.retriever import Retriever


class AskQuestionUseCase:
    """
    Coordinates the complete Retrieval-Augmented Generation (RAG)
    workflow for answering a user's question inside a Study Room.
    """

    def __init__(
        self,
        retriever: Retriever,
        prompt_builder: ChatPromptBuilder,
        llm: LLMPort,
    ) -> None:
        self._retriever = retriever
        self._prompt_builder = prompt_builder
        self._llm = llm

    def execute(
        self,
        question: str,
        study_room_id: str,
    ) -> str:
        """
        Executes the complete RAG pipeline.
        """

        contexts = self._retriever.retrieve(
            question=question,
            study_room_id=study_room_id,
        )

        system_prompt, user_prompt = (
            self._prompt_builder.build(
                question=question,
                contexts=contexts,
            )
        )

        return self._llm.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )
