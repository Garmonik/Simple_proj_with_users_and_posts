from django.db import models


class CreationTime(models.Model):
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        abstract = True


class UpdationTime(models.Model):
    updated = models.DateTimeField(auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True


class LastUpdateTime(CreationTime):
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
