from django.contrib import admin
from django.urls import path, include

import posts.views

urlpatterns = [
    path('posts/', posts.views.PostListView.as_view()),
    path('posts/create/', posts.views.PostCreateView.as_view()),
    path('posts/<int:pk>/', posts.views.PostView.as_view()),
    path('posts/update/<int:pk>/', posts.views.PostUpdateDeleteView.as_view()),
    path('posts/author/<int:author_id>/', posts.views.AuthorPostListView.as_view()),

    path('posts/like/<int:pk>/', posts.views.LikeView.as_view()),
    path('posts/bookmark/<int:pk>/', posts.views.BookmarkView.as_view()),
    path('posts/bookmark/list/', posts.views.PostBookmarkListView.as_view()),

]