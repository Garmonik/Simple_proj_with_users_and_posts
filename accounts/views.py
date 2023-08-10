from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts import swagger_helper_serializer
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from social_media.permissions import LoggedIn, IsVerificated


@extend_schema(
    methods=['PUT'],
    request=swagger_helper_serializer.UserProfileUpdateSerializer,
    responses={
        200: UserProfileSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]
    parser_classes = [MultiPartParser]

    def get_object(self):
        return self.request.user


@extend_schema(
    methods=['GET'],
    responses={
        200: UserProfileSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
    },
)
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]
    parser_classes = [MultiPartParser]

    def get(self, request, pk):
        user_profile = get_object_or_404(UserProfile, pk=pk, is_verified=True, is_active_status=True)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['GET'],
    responses={
        200: UserProfileSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def get_queryset(self):
        return UserProfile.objects.filter(is_verified=True, is_active_status=True)


@extend_schema(
    methods=['GET'],
    responses={
        200: UserProfileSerializer,
        404: swagger_helper_serializer.Error404Serializer,
    },
)
class MyUserProfileView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]
    parser_classes = [MultiPartParser]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, pk=request.user.pk, is_verified=True, is_active_status=True)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['DELETE'],
    responses={
        204: swagger_helper_serializer.Success204Serializer,
        404: swagger_helper_serializer.Error404Serializer,
    },
)
class UserProfileDeleteView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]
    parser_classes = [MultiPartParser]

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, pk=request.user.pk)
        user_profile.is_active_status = False
        user_profile.save()
        return Response({"success": "Your account has been deactivated"}, status=status.HTTP_204_NO_CONTENT)
