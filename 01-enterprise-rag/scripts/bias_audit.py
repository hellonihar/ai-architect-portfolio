#!/usr/bin/env python
"""
Audit document chunks for potential bias in language.
Usage: python scripts/bias_audit.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enterprise_rag.settings")

import django
django.setup()

from apps.ingestion.models import Chunk

BIAS_KEYWORDS = {
    "gender": ["he always", "she always", "manpower", "female doctor", "male nurse"],
    "age": ["too old", "too young", "overqualified", "digital native"],
    "race": ["articulate", "well-spoken", "aggressive", "passive"],
}


def run_audit():
    flagged = []
    for chunk in Chunk.objects.all():
        text_lower = chunk.content.lower()
        for category, keywords in BIAS_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    flagged.append({
                        "chunk_id": chunk.id,
                        "document_id": str(chunk.document_id),
                        "category": category,
                        "keyword": kw,
                        "snippet": chunk.content[:200],
                    })
    print(f"Audit complete. {len(flagged)} potential issues found.")
    for f in flagged:
        print(f"  [{f['category']}] '{f['keyword']}' in chunk {f['chunk_id']}: {f['snippet']}")
    return flagged


if __name__ == "__main__":
    run_audit()
