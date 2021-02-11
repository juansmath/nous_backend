from rest_framework import viewsets
from rest_framework import generics

from apps.usuario.models import Usuario
from apps.usuario.api.serializer import UsuarioSerializer

class UsuarioListApiView(generics.ListApiView):
    serializer_class = UsuarioSerializer

    def def get_queryset(self):
        return Usuario.objects.filter(estado = True)
