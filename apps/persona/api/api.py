import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import PersonaSerializer, PersonaDetalleSerializer

from apps.persona.models import Persona

class PersonaViewSet(viewsets.ViewSet):
    model = Persona
    serializer_class = PersonaSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save()

    def perform_update(self, serializer):
        if serializer.is_valid():
            error = serializer.errors
            serializer.save()
        else:
            validar_error = True
            error = serializer.errors

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer_persona = self.serializer_class(data=request.data)
        serializer_persona.is_valid(raise_exception=True)
        self.perform_create(serializer_persona)
        return Response(serializer_persona.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        persona_data = self.model.objects.filter(id = kwargs['pk'], estado = True).first()
        print(persona_data)
        if not persona_data:
            return Response({'Error':'No existe este usuario con estos datos!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_persona = self.serializer_class(persona_data, request.data)
        self.perform_update(serializer_persona)
        return Response(serializer_persona.data, status=status.HTTP_201_CREATED)