from django.contrib.auth import get_user_model
from django.db import models

from common.models import TimeStampedModel

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=200, blank=True, null=True)
    profile_img = models.ImageField(upload_to='users/profile_images', default='blank-profile-picture.png')

    def __str__(self) -> str:
        return str(self.user_id) + "-profile"


class Follow(TimeStampedModel):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followees")

    def __str__(self) -> str:
        return str(self.follower_id) + " follows " + str(self.followee_id)

    class Meta:
        # unique_together
        constraints = [
            models.UniqueConstraint(
                fields=['followee_id', 'follower_id'], name='unique_follow'
            )
        ]
