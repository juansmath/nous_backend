from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.general_serializer import *

from apps.prueba.models import Modulo, Competencia, NivelEjecucion, DescripcionNivelEjecucion

class ModuloViewSet(viewsets.ViewSet):
    model = Modulo
    serializer_class = ModuloSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class CompetenciaViewSet(viewsets.ViewSet):
    model = Competencia
    serializer_class = CompetenciaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class NivelEjecucionViewSet(viewsets.ViewSet):
    model = NivelEjecucion
    serializer_class = NivelEjecucionSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class DescripcionNivelEjecucionViewSet(viewsets.ViewSet):
    model = DescripcionNivelEjecucion
    serializer_class = DescripcionesNivelesEjecucionSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

