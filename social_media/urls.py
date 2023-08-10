from django.contrib import admin
from django.urls import path, include

api_patterns = [
    path('', include('posts.urls')),
    path('', include('accounts.urls')),
    path('', include('facecontrol.urls')),
    path('', include('social_media.schema_urls')),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]
