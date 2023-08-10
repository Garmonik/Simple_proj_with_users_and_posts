from django.core.exceptions import PermissionDenied
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import UserProfile
from social_media.permissions import LoggedIn, IsVerificated
from . import swagger_helper_serializer
from .models import Post, Like, Bookmark
from .serializers import PostSerializer, PostListSerializer


@extend_schema(
    methods=['GET'],
    responses={
        200: PostListSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class PostListView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def get(self, request):
        posts = Post.objects.annotate(count_likes=Count('likes'))
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['POST'],
    request=swagger_helper_serializer.PostSwaggerSerializer,
    responses={
        200: PostSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class PostCreateView(APIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    methods=['DELETE'],
    request=swagger_helper_serializer.PostSwaggerSerializer,
    responses={
        204: '',
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
        403: swagger_helper_serializer.Error404Serializer,

    },
)
@extend_schema(
    methods=['PUT'],
    request=swagger_helper_serializer.PostSwaggerSerializer,
    responses={
        200: PostSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
        403: swagger_helper_serializer.Error404Serializer,
    },
)
class PostUpdateDeleteView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def check_author(self, post):
        if post.owner != self.request.user:
            raise PermissionDenied("You do not have permission to perform this action.")

    def perform_update(self, serializer):
        post = self.get_object()
        self.check_author(post)
        serializer.save()

    def perform_destroy(self, instance):
        self.check_author(instance)
        instance.delete()


@extend_schema(
    methods=['GET'],
    request=swagger_helper_serializer.PostSwaggerSerializer,
    responses={
        200: PostListSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer,
    },
)
class PostView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        post = post.annotate(count_likes=Count('likes'))
        serializer = PostListSerializer(post, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    methods=['GET'],
    responses={
        200: PostListSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
    },
)
class AuthorPostListView(generics.ListAPIView):
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        queryset = Post.objects.filter(owner_id=author_id)
        queryset = queryset.filter(owner__is_verified=True, owner__is_active_status=True)
        queryset = queryset.annotate(count_likes=Count('likes'))
        return queryset


@extend_schema(
    methods=['POST'],
    responses={
        201: swagger_helper_serializer.PostLikeSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer
    },
)
@extend_schema(
    methods=['DELETE'],
    responses={
        204: swagger_helper_serializer.PostLike204Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer
    },
)
class LikeView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({'error': "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
        like = Like.objects.create(post=post, user=request.user)
        return Response({"success": "You like this post", "like": like.id}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        like = get_object_or_404(Like, user=request.user, post=post)
        like.delete()
        return Response({"success": "You like is delete"}, status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    methods=['POST'],
    responses={
        201: swagger_helper_serializer.PostBookmarkSerializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer
    },
)
@extend_schema(
    methods=['DELETE'],
    responses={
        204: swagger_helper_serializer.PostLike204Serializer,
        400: swagger_helper_serializer.ErrorSerializer,
        404: swagger_helper_serializer.Error404Serializer
    },
)
class BookmarkView(APIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if Bookmark.objects.filter(user=request.user, post=post).exists():
            return Response({'error': "This post already in you bookmark"}, status=status.HTTP_400_BAD_REQUEST)
        bookmark = Bookmark.objects.create(post=post, user=request.user)
        return Response({"success": "This post in you bookmark", "bookmark": bookmark.id}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        bookmark = get_object_or_404(Bookmark, user=request.user, post=post)
        bookmark.delete()
        return Response({"success": "Post exit your bookmark"}, status=status.HTTP_204_NO_CONTENT)


class PostBookmarkListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, LoggedIn, IsVerificated]
    serializer_class = PostListSerializer

    def get_queryset(self):
        qs = Post.objects.filter(bookmarks__user=self.request.user)
        qs = qs.annotate(count_likes=Count('likes'))
        return qs