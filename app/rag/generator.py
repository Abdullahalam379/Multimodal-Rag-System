from openai import OpenAI
from time import perf_counter

from monitoring.metrics import LLM_RESPONSE_TIME
from app.config.settings import settings

SYSTEM_PROMPT = """
You are a helpful AI assistant that answers questions based ONLY on the provided document context.

Instructions:
- Use only the retrieved context.
- If the answer is not present in the context, say:
  "I couldn't find that information in the provided documents."
- Do not make up facts.
- Answer clearly and concisely.
""".strip()


class Generator:
    """
    Generates answers using retrieved document context.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    def answer(self, question: str, context: str) -> str:
        """
        Generate an answer for a user's question.

        Args:
            question: User question.

        Returns:
            Generated answer.
        """
        start = perf_counter()



        user_prompt = f"""
Context:
{context}

Question:
{question}

Answer:
""".strip()

        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            temperature=0,
        )
        LLM_RESPONSE_TIME.observe(perf_counter() - start)
        return response.choices[0].message.content