from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'second_name',
            'phone_number',
            'birthday',
            'vk_link',
            'telegram_link',
            'instagram_link',
            'my_site_link',
            'github_link',
            'avatar'
        )