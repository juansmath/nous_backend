from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.response import Response


from apps.usuario.models import Usuario
from apps.usuario.api.serializers.usuario_serializer import UsuarioSerializer

class UsuarioViewSet(viewsets.ViewSet):
    serializer_class = UsuarioSerializer
    model = Usuario

    def get_queryset(self, pk=None):
        if pk != None:
            return self.model.objects.filter(id = pk, estado = True).first()
        else:
            return self.model.objects.filter(is_active = True)

    def list(self, request):
        usuarios = self.get_queryset()
        usuario_serializer = self.serializer_class(usuarios, many = True)
        return Response(usuario_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        usuario_serializer = self.serializer_class(data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response({'mensaje': 'Bienvenido, ya eres parte de NOUS, inicia sesión'},status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'Hubo un error al crear el usuario', 'error': usuario_serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer