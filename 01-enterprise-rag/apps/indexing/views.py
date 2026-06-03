from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.retriever import HybridRetriever


class SearchAPI(APIView):
    def get(self, request):
        query = request.query_params.get("q", "")
        top_k = int(request.query_params.get("top_k", 10))
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)

        retriever = HybridRetriever()
        results = retriever.retrieve(query, top_k=top_k)

        return Response({"query": query, "results": results, "total": len(results)})
