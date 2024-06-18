from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated


from core.models import User
from core.rest.serializers.profile import UserDetailSerializer, UserListSerializer


class UserListView(ListCreateAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        users = User.objects.all()
        return users


class UserDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = User.objects.get(pk=self.request.user.pk)
        # user = User.objects.first()
        return user
