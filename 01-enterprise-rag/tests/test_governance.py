from django.test import TestCase
from apps.governance.models import AuditLog


class AuditLogTest(TestCase):
    def test_create_audit_log(self):
        log = AuditLog.objects.create(
            action="DOCUMENT_UPLOADED",
            resource_type="Document",
            resource_id="123",
            user="testuser",
            details={"title": "Test"},
        )
        self.assertEqual(log.action, "DOCUMENT_UPLOADED")
        self.assertIsNotNone(log.timestamp)

    def test_audit_log_str(self):
        log = AuditLog.objects.create(
            action="CHAT_QUERY",
            resource_type="Chat",
            user="testuser",
        )
        self.assertIn("CHAT_QUERY", str(log))
        self.assertIn("testuser", str(log))

    def test_action_choices(self):
        valid_actions = [choice[0] for choice in AuditLog.ACTION_CHOICES]
        self.assertIn("DOCUMENT_UPLOADED", valid_actions)
        self.assertIn("CHAT_QUERY", valid_actions)
