from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import ProgramaSerializer, FacultadSerializer, NivelAcademicoSerializer
from apps.institucional.models import Programa, Facultad, NivelAcademico

class ProgramaViewSet(viewsets.ViewSet):
    model = Programa
    serializer_class = ProgramaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class FacultadViewSet(viewsets.ViewSet):
    model = Facultad
    serializer_class = FacultadSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

class NivelAcademicoViewSet(viewsets.ViewSet):
    model = NivelAcademico
    serializer_class = NivelAcademicoSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)