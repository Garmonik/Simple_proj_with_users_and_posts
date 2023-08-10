from django.contrib.auth.hashers import make_password
from drf_spectacular.utils import extend_schema
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import hashlib

from accounts.models import UserProfile
from facecontrol import swagger_helper_serializer
from facecontrol.mailer import send_confirmation_email, send_password_recovery_email
from facecontrol.models import CodeEmail
from social_media.helpfull import validation_username, validation_password, validate_email_format
from social_media.permissions import LoggedIn


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.RegisterSerializer,
    responses={
        201: swagger_helper_serializer.Register201Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class RegisterView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        password_again = request.data.get('password_again')
        email = request.data.get('email')

        username_errors = validation_username(username)
        password_errors = validation_password(password, password_again)
        email_errors = validate_email_format(email)

        all_errors = []
        if username_errors:
            all_errors += username_errors
        if password_errors:
            all_errors += password_errors
        if email_errors:
            all_errors += email_errors

        if all_errors:
            return Response({"error": all_errors}, status=status.HTTP_400_BAD_REQUEST)
        if UserProfile.objects.filter(username=username) or UserProfile.objects.filter(email=email):
            return Response({"error": "A user with the same username or email address already exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserProfile.objects.create(username=username, email=email, password=make_password(password))
            send_confirmation_email(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            return Response({"success": "Account created successfully, please check your email!", "email": email, "username": username, 'access_token': str(access_token)}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": "Some problems"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.VerificationSerializer,
    responses={
        200: swagger_helper_serializer.Verification200Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
        403: swagger_helper_serializer.Error403Serializer
    },
)
class VerificationView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        authorization_header = request.headers.get('Authorization', '')
        access_token_string = authorization_header.split()[1] if len(authorization_header.split()) > 1 else None
        if access_token_string:
            try:
                access_token = AccessToken(access_token_string)
                user_id = access_token['user_id']
                user = get_object_or_404(UserProfile, id=user_id)
                if user.is_verified:
                    return Response({"error": "You are already verified"}, status=status.HTTP_400_BAD_REQUEST)
                code = request.data.get('code')
                check_res = CodeEmail.objects.filter(code=code, email=user.email).latest('created')
                if check_res:
                    user.is_verified = True
                    user.save()
                    check_res.delete()
                    return Response({"success": "Account are verified!"}, status=status.HTTP_200_OK)
            except:
                return Response({"errors": "Some problems with token"}, status=status.HTTP_403_FORBIDDEN)


@extend_schema(
    methods=['PUT'],
    request=swagger_helper_serializer.PasswordRecoverySerializer,
    responses={
        200: swagger_helper_serializer.Verification200Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer
    },
)
class PasswordRecoveryView(APIView):
    parser_classes = [JSONParser]

    def put(self, request):
        email = request.data.get('email')
        email_errors = validate_email_format(email)
        if email_errors:
            return Response({"errors": email_errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = get_object_or_404(UserProfile, email=email)
            send_password_recovery_email(request, user)
            return Response({"success": "Please check your email!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Some problems"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.LoginSerializer,
    responses={
        200: swagger_helper_serializer.Login200Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
    },
)
class LoginView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_object_or_404(UserProfile, email=email)
        hashed_password = user.password
        try:
            if hashlib.sha256(password.encode('utf-8')).hexdigest() == hashed_password:
                return Response({"error": "Enter correct data"}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"access_token": access_token, "refresh_token": str(refresh)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Some problems"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['PUT'],
    request=swagger_helper_serializer.ChangePasswordSerializer,
    responses={
        200: swagger_helper_serializer.Verification200Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class ChangePasswordView(APIView):
    parser_classes = [MultiPartParser]
    permission_classes = [LoggedIn]

    def put(self, request):
        password = request.data.get('password')
        password_new = request.data.get('password_new')
        password_new_again = request.data.get('password_new_again')

        password_errors = validation_password(password_new, password_new_again)
        if password_errors:
            return Response({"error": password_errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if hashlib.sha256(password.encode('utf-8')).hexdigest() == request.user.password:
                request.user.password = make_password(password_new)
                request.user.save()
                return Response({"success": "Password changed!"}, status=status.HTTP_200_OK)
            return Response({"error": "Enter correct data"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Some problems"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.RefreshTokenSerializer,
    responses={
        200: swagger_helper_serializer.Login200Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class RefreshTokenView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"access_token": access_token, "refresh_token": str(refresh)}, status=status.HTTP_200_OK)

