import time
from django.utils.deprecation import MiddlewareMixin
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "endpoint"])
TOKEN_USAGE = Counter("llm_tokens_total", "Total LLM tokens consumed", ["model", "operation"])
DRIFT_SCORE = Histogram("retrieval_drift_score", "Retrieval drift score distribution")


class MetricsMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request._start_time = time.time()
        return None

    def process_response(self, request, response):
        if hasattr(request, "_start_time"):
            latency = time.time() - request._start_time
            endpoint = request.path
            REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(latency)
            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=response.status_code).inc()
        return response
