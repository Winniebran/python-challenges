from rest_framework.views import APIView, Response, Request, status
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsUserEmployee
from django.shortcuts import get_object_or_404


class UserView(APIView):
    def post(self, request: Request) -> Response:
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsUserEmployee]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)
        self.check_object_permissions(request, user)

        user_serializer = UserSerializer(user, request.data, partial=True)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()

        return Response(user_serializer.data, status.HTTP_200_OK)
