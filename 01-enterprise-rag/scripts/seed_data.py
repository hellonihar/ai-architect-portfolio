#!/usr/bin/env python
"""
Seed database with sample documents for development.
Usage: python scripts/seed_data.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enterprise_rag.settings")

import django
django.setup()

from apps.ingestion.models import Document


SAMPLE_DOCUMENTS = [
    {"title": "Employee Onboarding Guide", "content": "Welcome to the company! This guide covers the onboarding process..."},
    {"title": "IT Security Policy 2026", "content": "All employees must follow these security guidelines. Passwords must be..."},
    {"title": "Product Roadmap Q2-Q4", "content": "Our product roadmap for the next three quarters includes..."},
]


def seed():
    for doc_data in SAMPLE_DOCUMENTS:
        doc, created = Document.objects.get_or_create(
            title=doc_data["title"],
            defaults={"status": "pending"},
        )
        if created:
            print(f"Created: {doc.title}")
        else:
            print(f"Exists: {doc.title}")
    print("Seeding complete.")


if __name__ == "__main__":
    seed()
