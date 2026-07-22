from app.infrastructure.ai.prompts.base_prompt_builder import (
    BasePromptBuilder,
)


class ExamPromptBuilder(BasePromptBuilder):
    """
    Prompt builder for generating academic exams
    from retrieved document context.
    """

    SYSTEM_PROMPT = """
You are an academic assistant specialized in creating exams.

Rules:

- Use ONLY the provided context.
- Never invent information.
- Never use external knowledge.
- Return ONLY valid JSON.
- Do not include markdown.
- Do not include explanations outside the JSON.

Generate three types of questions:

1. Multiple Choice
2. True / False
3. Open Answer

Every question must include its correct answer.

JSON format:

{
  "title": "...",
  "questions": [
    {
      "type": "multiple_choice",
      "question": "...",
      "options": [
        "...",
        "...",
        "...",
        "..."
      ],
      "correct_answer": "...",
      "explanation": "..."
    },
    {
      "type": "true_false",
      "question": "...",
      "correct_answer": true,
      "explanation": "..."
    },
    {
      "type": "open",
      "question": "...",
      "correct_answer": "...",
      "explanation": "..."
    }
  ]
}
""".strip()

    def build(
        self,
        contexts: list[dict],
        multiple_choice: int = 5,
        true_false: int = 3,
        open_questions: int = 2,
    ) -> tuple[str, str]:
        """
        Builds the prompt used to generate academic exams.
        """

        context_text = self.build_context(
            contexts,
        )

        total_questions = (
            multiple_choice
            + true_false
            + open_questions
        )

        user_prompt = f"""
Using ONLY the following context, generate an academic exam.

Requirements:

- Total questions: {total_questions}
- Multiple choice: {multiple_choice}
- True/False: {true_false}
- Open answer: {open_questions}

Context:

{context_text}
""".strip()

        return (
            self.SYSTEM_PROMPT,
            user_prompt,
        )
