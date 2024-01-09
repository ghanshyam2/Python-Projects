from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)

    thumbnail = models.ImageField(upload_to='blog/thumbnails', default='no-thumbnail.jpeg')
    description = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return str(self.auther) + '-' + str(self.title)

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"pk": self.pk})

