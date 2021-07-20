from rest_framework.authentication import get_authorization_header
from apps.usuario.authentication import ExpiringTokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

def get_usuario(request):
    token = get_authorization_header(request).split()
    if token:
        token = token[1].decode()
        token_expired = ExpiringTokenAuthentication()
        try:
            user,_ = token_expired.authenticate_credentials(token)
        except:
            return None
        return user
    return None

class Authentication(object):
    def dispatch(self, request, *args, **kwargs):
        user = get_usuario(request)
        if user is not None:
            if user.is_authenticated:
                return super().dispatch(request, *args, **kwargs)
            return Response({'error': 'No ha iniciado sesión con este usuario.'}, status=status.HTTP_403_FORBIDDEN)
        response = Response({'error': 'No se ha encontrado un usuario con estos datos.'}, status=status.HTTP_403_FORBIDDEN)
        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}
        return response