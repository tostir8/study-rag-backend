from app.infrastructure.ai.prompts.base_prompt_builder import (
    BasePromptBuilder,
)


class ChatPromptBuilder(BasePromptBuilder):
    """
    Prompt builder used by the conversational RAG.

    The assistant must answer only from the retrieved
    document context and never invent information.
    """

    SYSTEM_PROMPT = """
You are an AI academic assistant.

Your only source of truth is the retrieved context.

Rules:

- Answer ONLY using the provided context.
- Never invent facts.
- Never use external knowledge.
- If the answer is not present in the context,
  clearly state that the information is unavailable.
- Keep answers clear, concise and academically correct.
""".strip()

    def build(
        self,
        question: str,
        contexts: list[dict],
    ) -> tuple[str, str]:
        """
        Builds the prompt for conversational RAG.
        """

        context_text = self.build_context(
            contexts,
        )

        user_prompt = f"""
Context:

{context_text}

Question:

{question}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )
