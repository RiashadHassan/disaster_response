from django.urls import path, include

urlpatterns = [
    path("", include("core.rest.urls.profile")),
]
