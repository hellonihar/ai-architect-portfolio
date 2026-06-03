from prometheus_client import start_http_server, REGISTRY
from django.conf import settings


def start_metrics_server():
    port = settings.PROMETHEUS_METRICS_PORT
    start_http_server(port)
    return port


def get_metrics():
    return generate_latest(REGISTRY)
