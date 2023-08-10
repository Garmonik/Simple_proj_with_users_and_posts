from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import UserProfile


class LoggedIn(BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.headers.get('Authorization', '')
            access_token_string = authorization_header.split()[1] if len(authorization_header.split()) > 1 else None
            if access_token_string:
                access_token = AccessToken(access_token_string)
                user_id = access_token['user_id']
                request.user = UserProfile.objects.get(id=user_id)
                return bool(user_id)
            return False
        except:
            return False


class IsVerificated(BasePermission):
    def has_permission(self, request, view):
        try:
            authorization_header = request.headers.get('Authorization', '')
            access_token_string = authorization_header.split()[1] if len(authorization_header.split()) > 1 else None
            if access_token_string:
                access_token = AccessToken(access_token_string)
                user_id = access_token['user_id']
                request.user = UserProfile.objects.get(id=user_id)
                if user_id and request.user.is_verified:
                    return True
            return False
        except:
            return False
