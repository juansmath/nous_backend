import json

from django.db import connection
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser

from apps.base.api import BaseViewSet
from apps.prueba.models import (Modulo, Competencia, OpcionRespuesta, GrupoPreguta, OpcionEnunciado,
                                Justificacion, Pregunta, BancoPregunta, Prueba, ResultadoPrueba)

from apps.prueba.api.serializers import (ModuloSerializer, CompetenciaSerializer, OpcionrespuestaSerializer,
                                         GrupoPreguntaSerializer, OpcionEnunciadoSerializer, JustificacionSerializer,
                                         PreguntaSerilaizer, BancoPreguntaSerializer, PruebaSerializer, ResultadoPruebaSerializer)

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
    serializer_class = OpcionrespuestaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class GrupoPreguntaViewSet(viewsets.ViewSet):
    model = GrupoPreguta
    serializer_class = GrupoPreguntaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

