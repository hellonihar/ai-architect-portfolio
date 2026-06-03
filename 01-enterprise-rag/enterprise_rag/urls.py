from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/ingestion/", include("apps.ingestion.urls")),
    path("api/indexing/", include("apps.indexing.urls")),
    path("api/chat/", include("apps.chat.urls")),
    path("api/governance/", include("apps.governance.urls")),
]
