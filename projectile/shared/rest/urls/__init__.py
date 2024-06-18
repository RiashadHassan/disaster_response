from django.urls import path, include

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("", include("shared.rest.urls.auth")),
    path("", include("shared.rest.urls.swagger")),
]
