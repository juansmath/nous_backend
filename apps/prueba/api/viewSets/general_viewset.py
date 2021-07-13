from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.general_serializer import *

from apps.prueba.models import Modulo, Competencia, OpcionRespuesta, NivelEjecucion, DescripcionNivelEjecucion, NivelDificultad

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

class OpcionRespuestaViewSet(viewsets.ViewSet):
    model = OpcionRespuesta
    serializer_class = OpcionRespuestaSerializer

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
    serializer_class = DescripcionNivelEjecucionSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class NivelDificultadViewSet(viewsets.ViewSet):
    model = NivelDificultad
    serializer_class = NivelDificultadSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

