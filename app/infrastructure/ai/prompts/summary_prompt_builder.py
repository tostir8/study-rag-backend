from app.infrastructure.ai.prompts.base_prompt_builder import (
    BasePromptBuilder,
)


class SummaryPromptBuilder(BasePromptBuilder):
    """
    Prompt builder for generating academic summaries
    from retrieved document context.
    """

    SYSTEM_PROMPT = """
You are an academic assistant specialized in producing study summaries.

Rules:

- Use ONLY the provided context.
- Never invent information.
- Never add external knowledge.
- Organize the summary clearly.
- Highlight the most important concepts.
- Use concise academic language.
- If there is not enough information,
  explicitly say so.
""".strip()

    def build(
        self,
        contexts: list[dict],
    ) -> tuple[str, str]:
        """
        Builds the prompt used to generate summaries.
        """

        context_text = self.build_context(
            contexts,
        )

        user_prompt = f"""
Using ONLY the following context, generate a clear academic summary.

Context:

{context_text}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )
