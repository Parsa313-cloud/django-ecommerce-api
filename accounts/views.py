from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse



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
            "login_url": reverse("login"),
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

        return User.objects.filter(id=user.id)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff:
            return obj
        if obj != user:
            raise PermissionDenied("You don’t have permission to access this user.")

        return obj

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Please provide username and password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Incorrect username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        if not user.is_active:
            return Response({"error": "User account is disabled."}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        data = {
            "username": user.username,
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "User successfully logged in."
        }
        return Response(data, status=status.HTTP_200_OK)