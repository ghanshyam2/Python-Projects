from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path("", UploadPostView.as_view(), name="upload-post"),
    path('edit/<int:pk>/', PostEditView.as_view(), name='post-edit'),
    path("<slug:uuid>/", PostDetail.as_view(), name="post-detail"),
    path("<slug:uuid>/comments/", PostCommentView.as_view(), name="post-comment"),
    path('del/<int:pk>', PostDeleteView.as_view(), name="post-delete"),
    path("<slug:uuid>/like_dislike/", LikeDislikePostView.as_view(), name="post-like-dislike"),
    #path("<slug:uuid>/", views.PostDetail.as_view(), name="post-detail"),
    #path("<slug:uuid>/comments/", views.PostCommentView.as_view(), name="post-comment"),
    #path("<slug:uuid>/like_dislike/", views.LikeDislikePostView.as_view(), name="post-like-dislike")
]