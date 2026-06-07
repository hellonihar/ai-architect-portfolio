from functools import lru_cache

from core.config import settings


@lru_cache
def get_settings() -> settings.__class__:
    return settings
