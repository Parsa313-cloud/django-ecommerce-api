from django.contrib.auth import authenticate
from rest_framework.views import APIView, Response
from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.urls import reverse


from .serializers import UserSignUpSerializer, ProfileSerializer, UserSerializer
from .models import User, Profile

# Create your views here.

# sign up view :


class SignUpView(APIView):
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "username": user.username,
            "email": user.email,
            "message": "User created",
            "login_url": reverse('login'),
        }, status=status.HTTP_201_CREATED)



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]


    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)





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

        return User.objects.filter(user=user.id)

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        if user.is_staff:
            return obj
        if obj != user:
            raise PermissionDenied(
                "You don’t have permission to access this user.")
        return obj
