from django.db import models
from django.contrib.auth.models import User
from social_media.base import CreationTime, UpdationTime


class UserProfile(User, CreationTime, UpdationTime, models.Model):

    is_verified = models.BooleanField(default=False)
    is_active_status = models.BooleanField(default=True)

    description = models.CharField(max_length=500, null=True, blank=True)

    vk_link = models.CharField(max_length=500, null=True, blank=True)
    telegram_link = models.CharField(max_length=500, null=True, blank=True)
    instagram_link = models.CharField(max_length=500, null=True, blank=True)
    my_site_link = models.CharField(max_length=500, null=True, blank=True)
    github_link = models.CharField(max_length=500, null=True, blank=True)

    avatar = models.ImageField(null=True, blank=True, upload_to='static/avatars/')

    second_name = models.CharField(max_length=250, null=True, blank=True)

    phone_number = models.CharField(max_length=12, null=True, blank=True)

    birthday = models.DateField(null=True, blank=True)

    class Meta():
        verbose_name = 'UserProfile'

    def __str__(self):
        return f"{self.id}: {self.username}: {self.email}"


