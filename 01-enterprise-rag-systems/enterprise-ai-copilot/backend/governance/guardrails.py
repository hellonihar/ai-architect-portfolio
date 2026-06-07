import re
import logging

from core.config import settings

logger = logging.getLogger(__name__)

SENSITIVE_PATTERNS = [
    r"\b\d{3}-\d{2}-\d{4}\b",
    r"\b\d{16}\b",
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    r"\b(?:\d{3}[-.]?)?\d{3}[-.]?\d{4}\b",
]


class InputGuard:
    def check(self, text: str) -> tuple[bool, str | None]:
        if not text.strip():
            return False, "Query cannot be empty."
        if len(text) > settings.max_input_length:
            return False, f"Query exceeds maximum length of {settings.max_input_length} characters."
        for pattern in SENSITIVE_PATTERNS:
            if re.search(pattern, text):
                return False, "Query contains potentially sensitive information. Please remove it and try again."
        return True, None


class OutputGuard:
    def check(self, text: str) -> tuple[bool, str | None]:
        if not text.strip():
            return False, "Model returned an empty response."
        return True, None
