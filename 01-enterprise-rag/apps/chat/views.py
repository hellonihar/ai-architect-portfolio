from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from apps.indexing.services.retriever import HybridRetriever
from .prompts import SYSTEM_PROMPT
from apps.governance.models import AuditLog


class ChatAPI(APIView):
    def post(self, request):
        query = request.data.get("message", "")
        conversation_id = request.data.get("conversation_id")
        if not query:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve context
        retriever = HybridRetriever()
        context_chunks = retriever.retrieve(query, top_k=5)

        # Build context string
        context_text = "\n\n".join(
            f"[Source: {c['id']}] {c.get('text', '')}" for c in context_chunks
        )

        # Generate response via Groq
        llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL,
            temperature=0.3,
        )
        prompt = SYSTEM_PROMPT.format(context=context_text)
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": query},
        ]
        response = llm.invoke(messages)

        AuditLog.objects.create(
            action="CHAT_QUERY",
            resource_type="Chat",
            user=request.user.username if request.user.is_authenticated else "anonymous",
            details={"conversation_id": conversation_id, "query_length": len(query)},
        )

        return Response({
            "response": response.content,
            "sources": [c["id"] for c in context_chunks],
            "conversation_id": conversation_id,
        })
