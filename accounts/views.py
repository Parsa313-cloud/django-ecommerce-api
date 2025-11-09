from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from django.db import transaction


from .serializers import UserSignUpSerializer, ProfileSerializer, UserSerializer
from .models import User, Profile

# Create your views here.

# sign up view :


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "username": user.username,
            "email": user.email,
            "message": "User created",
            "login_url": "auth/login"
        }, status=status.HTTP_201_CREATED)


# profile view set :
class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Profile.objects.all()

        return Profile.objects.filter(user=user)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff:
            return obj
        if obj.user != user:
            raise PermissionDenied(
                "You don’t have permission to access this profile.")
        return obj

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# user view set :


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return User.objects.all()

        return User.objects.filter(user=user)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff:
            return obj
        if obj.user != user:
            raise PermissionDenied(
                "You don’t have permission to access this user.")
        return obj
