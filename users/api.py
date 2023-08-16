from django.contrib.auth import login
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework import views
from rest_framework.response import Response

from users.models import User
from users.serializer import UserSerializer, LoginSerializer


# Class based view to register user
class UserCreate(generics.CreateAPIView):
    """
    user create api
    post: return created user
    parameters : ["first_name", "last_name", "email", "username", 'password']
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    user list api
    get: return all created users list
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    user details, update and delete api
    get:
        Returns the detail of a user instance
        parameters: ["id"]
    put:
        Update the detail of a user instance
        parameters: ["id", "first_name", "last_name", "email", "username", 'password']
    delete:
        Delete a user instance
        parameters: ["id"]
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response("Logged-in Successfully!!!", status=status.HTTP_202_ACCEPTED)