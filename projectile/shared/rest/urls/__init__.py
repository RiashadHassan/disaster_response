from django.urls import path, include

urlpatterns = [
    path("", include("shared.rest.urls.auth")),
    path("", include("shared.rest.urls.swagger")),
]
