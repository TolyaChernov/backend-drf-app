from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import UserSerializer


class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            status.HTTP_201_CREATED: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                },
            )
        },
    )
    def post(self, request):
        """
        Register a new user.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data.get("email")
            password = validated_data.get("password")
            hashed_password = make_password(password)
            user = CustomUser.objects.create(
                email=email, password=hashed_password)
            return Response(
                {"id": user.id, "email": user.email}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "password"],
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(type=openapi.TYPE_STRING),
                    "access": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: "Invalid email or password",
        },
    )
    def post(self, request):
        """
        Log in an existing user.
        """
        email = request.data.get("email")
        password = request.data.get("password")
        make_password(password)
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)}
            )
        return Response(
            {"message": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class UserLogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["refresh"],
            properties={
                "refresh": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={
            status.HTTP_205_RESET_CONTENT: "Logout successful",
            status.HTTP_400_BAD_REQUEST: "Invalid token",
        },
    )
    def post(self, request):
        """
        Log out a user.
        """
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)

            # Add token to blacklist
            token.blacklist()

            return Response(
                {"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            print(e)
            return Response(
                {"message": f"Invalid token --- {e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["email", "old_password", "new_password"],
            properties={
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
                ),
                "old_password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD
                ),
            },
        ),
        responses={
            status.HTTP_200_OK: "Password changed successfully",
            status.HTTP_400_BAD_REQUEST: "Invalid email or password",
        },
    )
    def post(self, request):
        """
        Change user's password.
        """
        email = request.data.get("email")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        user = CustomUser.objects.filter(email=email).first()
        if user and user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully"})
        return Response(
            {"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST
        )
