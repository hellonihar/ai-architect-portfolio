from rest_framework import viewsets, permissions
from .models import AuditLog


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = super().get_queryset()
        action = self.request.query_params.get("action")
        user = self.request.query_params.get("user")
        if action:
            qs = qs.filter(action=action)
        if user:
            qs = qs.filter(user=user)
        return qs
