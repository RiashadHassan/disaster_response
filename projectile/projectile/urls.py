from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # django admin panel
    path("admin/", admin.site.urls),
    # swagger and other stuff
    path("", include("shared.rest.urls")),
    path("api/v1/me", include("core.rest.urls")),
    path("", include("disaster.rest.urls")),
    path("", include("response.rest.urls")),
    path("", include("emailio.rest.urls")),
]
