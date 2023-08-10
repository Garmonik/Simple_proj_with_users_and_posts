from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class Error404Serializer(serializers.Serializer):
    detail = serializers.CharField()


class PostSwaggerSerializer(serializers.Serializer):
    annotation = serializers.CharField()
    photo = serializers.ImageField()


class PostLikeSerializer(serializers.Serializer):
    success = serializers.CharField()
    like = serializers.IntegerField()


class PostBookmarkSerializer(serializers.Serializer):
    success = serializers.CharField()
    bookmark = serializers.IntegerField()


class PostLike204Serializer(serializers.Serializer):
    success = serializers.CharField()
