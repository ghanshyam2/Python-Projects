from django.db import models

from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel
import uuid

User = get_user_model()


class Tag(TimeStampedModel):
    title = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return "#" + self.title

    def clean(self) -> None:
        self.title = self.title.lower()
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class Post(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/post_images')
    caption = models.TextField()
    like_count = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, related_name="posts", through="PostTag")

    def __str__(self) -> str:
        return str(self.id) + " posted by " + str(self.user_id)


class PostLike(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_likes")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["post_id", "user_id"], name="unique_user_post_like"
            )
        ]

    def __str__(self) -> str:
        return str(self.post_id) + " liked by " + str(self.user_id)


class Comment(TimeStampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies")
    details = models.TextField(default=None)


class PostTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tag_id", "post_id"], name="unique_post_tag"
            )
        ]

    def __str__(self) -> str:
        return str(self.tag_id) + ' taged on ' + str(self.post_id)
