from datetime import timedelta, datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.sessions.models import Session
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

def expires_in(token):
    time_elapsed  = timezone.now() - token.created
    return timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

def is_token_expired(token):
    return expires_in(token) < timedelta(seconds=0)

def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        sesiones = Session.objects.filter(expire_date__gte=datetime.now())
        user  = token.user
        if sesiones:
            for sesion in sesiones:
                sesion_data = sesion.get_decoded()
                if user.id == int(sesion_data.get('_auth_user_id')):
                    sesion.delete()
        token.delete()

    return is_expired

class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.select_related('user').get(key=key)
        except:
            raise AuthenticationFailed('El token no es valido!')

        if not token.user.is_active:
            raise AuthenticationFailed('El usuario no esta activo!')

        is_espired = token_expire_handler(token)
        if is_espired:
            raise AuthenticationFailed('Su token ha expirado!')

        return (token.user, token)