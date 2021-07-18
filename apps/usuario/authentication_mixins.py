from rest_framework.authentication import get_authorization_header
from .authentication import ExpiringTokenAuthentication

class Authentication(object):
    def get_user(self, request):
        token = get_authorization_header(request).split()
        if token:
            pass
    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)