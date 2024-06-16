from django.urls import path
from core.rest.views.profile import UserDetailView, UserListView

urlpatterns = [
    path("", UserDetailView.as_view(), name="me.profile"),
    path("/users", UserListView.as_view(), name="me.user-list"),
]
