from django.test import TestCase
from apps.ingestion.models import Document


class DocumentModelTest(TestCase):
    def test_create_document(self):
        doc = Document.objects.create(title="Test Doc")
        self.assertEqual(doc.status, "pending")
        self.assertIsNotNone(doc.uploaded_at)

    def test_document_str(self):
        doc = Document.objects.create(title="Test Doc")
        self.assertEqual(str(doc), "Test Doc")

    def test_default_status(self):
        doc = Document.objects.create(title="Test Doc")
        self.assertEqual(doc.status, "pending")
