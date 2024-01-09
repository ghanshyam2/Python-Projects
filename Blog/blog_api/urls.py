from django.urls import path
from .views import BlogList, BlogDetails, BlogCreateView, BlogUpdateView, BlogDeleteView

urlpatterns = [
    path("", BlogList.as_view(), name="home"),
    path("blog/<int:pk>/", BlogDetails.as_view(), name="blog_detail"),
    path("blog/new/", BlogCreateView.as_view(), name="blog_new"),
    path("blog/<int:pk>/edit", BlogUpdateView.as_view(), name="blog_edit" ),
    path('blog/<int:pk>/delete', BlogDeleteView.as_view(), name="blog_delete")
]
