class PromptBuilder:
    """
    Builds prompts for Retrieval-Augmented Generation (RAG).

    It combines the retrieved document context with
    the user's question to produce a prompt for the LLM.
    """

    SYSTEM_PROMPT = """
You are an AI study assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context,
say that the information is not available.

Be concise, accurate and factual.
""".strip()

    def build(
        self,
        question: str,
        contexts: list[dict],
    ) -> tuple[str, str]:
        """
        Builds the system prompt and user prompt.

        Args:
            question: User question.
            contexts: Retrieved chunks.

        Returns:
            Tuple containing:
                (system_prompt, user_prompt)
        """

        context_text = "\n\n".join(
            context["document"]
            for context in contexts
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
