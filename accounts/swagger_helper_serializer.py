from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class Error404Serializer(serializers.Serializer):
    detail = serializers.CharField()


class Success204Serializer(serializers.Serializer):
    success = serializers.CharField()

class UserProfileUpdateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    second_name = serializers.CharField()
    phone_number = serializers.CharField()
    birthday = serializers.DateField()
    vk_link = serializers.CharField()
    telegram_link = serializers.CharField()
    instagram_link = serializers.CharField()
    my_site_link = serializers.CharField()
    github_link = serializers.CharField()
    avatar = serializers.ImageField()