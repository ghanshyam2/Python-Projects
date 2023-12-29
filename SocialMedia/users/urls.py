from django.contrib import admin
from django.urls import path, include
from . import views
from posts.views import ListPosts
from .views import *
urlpatterns = [
    path("profile/<slug:username>/", GetProfileView.as_view(), name="profile"),
    #path('prof/edit/<slug:username>/', ProfileEditView.as_view(), name='edit-profile'),
    path("users/<slug:username>/follow/", FollowView.as_view(), name="follow"),
    path("users/<slug:username>/unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("users/<slug:username>/posts/", ListPosts.as_view(), name="list-user-posts")
]

# admin = admin123@gmail.com
# pass = admin
