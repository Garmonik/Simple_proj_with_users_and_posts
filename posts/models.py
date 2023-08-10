from django.db import models

from accounts.models import UserProfile
from social_media.base import LastUpdateTime, CreationTime


class Post(LastUpdateTime, models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="posts")
    annotation = models.TextField()
    photo = models.ImageField(null=True, blank=True, upload_to='static/posts/')

    def __str__(self):
        return f'Post {self.pk} by {self.owner.username}'


class Like(CreationTime, models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', db_index=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user.username} liked post #{self.post.pk}"


class Bookmark(CreationTime, models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmarks', db_index=True)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f"{self.user.username} bookmarked post #{self.post.pk}"

