from langchain_groq import ChatGroq

from core.config import settings


class GroqClient:
    def __init__(self):
        self.llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_model,
            temperature=settings.groq_temperature,
            max_tokens=2048,
        )

    def generate(self, prompt: str) -> str:
        return self.llm.invoke(prompt).content
