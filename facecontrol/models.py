from django.db import models
from social_media.base import CreationTime


class CodeEmail(CreationTime, models.Model):
    code = models.IntegerField(null=True)
    email = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.email}: {self.code}"

