from app.infrastructure.ai.prompts.base_prompt_builder import (
    BasePromptBuilder,
)


class FlashcardPromptBuilder(BasePromptBuilder):
    """
    Prompt builder for generating academic flashcards
    from retrieved document context.
    """

    SYSTEM_PROMPT = """
You are an academic assistant specialized in generating study flashcards.

Rules:

- Use ONLY the provided context.
- Never invent information.
- Never use external knowledge.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside the JSON.
- Every flashcard must contain one concept on the front
  and its explanation on the back.

JSON format:

{
  "flashcards": [
    {
      "front": "...",
      "back": "..."
    }
  ]
}
""".strip()

    def build(
        self,
        contexts: list[dict],
        amount: int = 10,
    ) -> tuple[str, str]:
        """
        Builds the prompt used to generate flashcards.
        """

        context_text = self.build_context(
            contexts,
        )

        user_prompt = f"""
Using ONLY the following context, generate {amount} study flashcards.

Context:

{context_text}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )
