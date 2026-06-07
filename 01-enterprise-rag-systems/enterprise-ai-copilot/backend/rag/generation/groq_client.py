from langchain_groq import ChatGroq

from core.config import settings


class GroqLLM:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=0.1,
            max_tokens=2048
        )

    def generate(self, prompt) -> str:
        response = self.llm.invoke(prompt)
        return response.content
