from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .tasks import process_document
from apps.governance.models import AuditLog


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        doc = serializer.save()
        process_document.delay(doc.id)
        AuditLog.objects.create(
            action="DOCUMENT_UPLOADED",
            resource_type="Document",
            resource_id=str(doc.id),
            user=self.request.user.username if self.request.user.is_authenticated else "anonymous",
            details={"title": doc.title},
        )

    @action(detail=True, methods=["post"])
    def reprocess(self, request, pk=None):
        doc = self.get_object()
        doc.status = "pending"
        doc.save()
        process_document.delay(doc.id)
        return Response({"status": "reprocessing"})
