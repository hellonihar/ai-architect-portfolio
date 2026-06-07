import logging

logger = logging.getLogger(__name__)


class FallbackHandler:
    def __init__(self, primary_llm, fallback_llm=None):
        self.primary = primary_llm
        self.fallback = fallback_llm

    def generate_with_fallback(self, prompt) -> str:
        try:
            return self.primary.generate(prompt)
        except Exception as e:
            logger.warning(f"Primary LLM failed: {e}")
            if self.fallback:
                return self.fallback.generate(prompt)
            return "I'm sorry, I'm unable to process your request at this time. Please try again later."
