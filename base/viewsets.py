from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.contrib.auth import logout, login, authenticate
from rest_framework import viewsets, views, response, status
from base import models, serializers


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer


class ToDoViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_authenticated is False:
            raise PermissionDenied
        return models.ToDo.objects.filter(user=self.request.user).all()

    serializer_class = serializers.ToDoSerializer


class SessionView(views.APIView):
    def get(self, request):
        user = request.user
        user_serializer = serializers.UserSerializer(user)
        user_data = user_serializer.data
        return response.Response(data=user_data)

    def post(self, request):
        serializer = serializers.SessionSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data["username"]
            password = serializer.data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                user_serializer = serializers.UserSerializer(user)
                user_data = user_serializer.data
                return response.Response(data=user_data, status=status.HTTP_201_CREATED)
        error_message = {"error": "Invalid username or password"}
        return response.Response(data=error_message, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        logout(request)
        return response.Response(data={}, status=status.HTTP_202_ACCEPTED)
