from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


class Error404Serializer(serializers.Serializer):
    detail = serializers.CharField()


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    password_again = serializers.CharField()


class Register201Serializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()
    success = serializers.CharField()
    access_token = serializers.CharField()


class VerificationSerializer(serializers.Serializer):
    code = serializers.IntegerField()


class Verification200Serializer(serializers.Serializer):
    success = serializers.CharField()


class Error403Serializer(serializers.Serializer):
    errors = serializers.CharField()


class PasswordRecoverySerializer(serializers.Serializer):
    email = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()


class Login200Serializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password_new = serializers.CharField()
    password_new_again = serializers.CharField()


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
