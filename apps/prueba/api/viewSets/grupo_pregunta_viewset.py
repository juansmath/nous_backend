from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.grupo_pregunta_serializer import GrupoPreguntaSerializer, GrupoPreguntaDetalleSerializer, EnunciadoGrupoPreguntaSerializer, EnunciadoGrupoPreguntaDetalleSerializer

from apps.prueba.models import GrupoPregunta, EnunciadoGrupoPregunta

class GrupoPreguntaViewSet(viewsets.ViewSet):
    model = GrupoPregunta
    serializer_class = GrupoPreguntaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)