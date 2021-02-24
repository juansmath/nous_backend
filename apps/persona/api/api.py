from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import PersonaSerializer, PersonaDetalleSerializer

from apps.persona.models import Persona

class PersonaViewSet(viewsets.ViewSet):
    model = Persona
    serializer_class = PersonaSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exeption = True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers=headers)