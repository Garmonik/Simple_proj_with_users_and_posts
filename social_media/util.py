import socket
from datetime import datetime
from django.conf import settings
from django.views.decorators import http


def require_http_methods(methods):
    if not settings.DEBUG:
        return http.require_http_methods(methods)
    return lambda x: x


def get_rfc5424_time():
    return f'{datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]}Z'


def get_rfc5424_hostname():
    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = '-'
    return hostname
