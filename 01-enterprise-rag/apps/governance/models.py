from django.db import models


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ("DOCUMENT_UPLOADED", "Document Uploaded"),
        ("DOCUMENT_DELETED", "Document Deleted"),
        ("CHAT_QUERY", "Chat Query"),
        ("SEARCH", "Search"),
        ("USER_LOGIN", "User Login"),
        ("PERMISSION_CHANGE", "Permission Change"),
    ]

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=100, blank=True)
    user = models.CharField(max_length=255)
    details = models.JSONField(default=dict)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["action"]),
            models.Index(fields=["user"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"
