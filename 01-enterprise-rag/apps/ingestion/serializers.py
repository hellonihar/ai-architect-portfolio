from rest_framework import serializers
from .models import Document, Chunk


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "title", "file", "status", "uploaded_at", "page_count"]
        read_only_fields = ["status", "uploaded_at", "page_count"]


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = ["id", "document", "content", "chunk_index", "metadata"]
