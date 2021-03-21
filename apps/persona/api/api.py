import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .serializers import PersonaSerializer, PersonaDetalleSerializer

from apps.persona.models import Persona

class PersonaViewSet(viewsets.ViewSet):
    model = Persona
    serializer_class = PersonaSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.model.objects.filter(estado = True)
        return self.model.objects.filter(id = pk, estado = True).first()

    def perform_create(self, serializer):
        if serializer.is_valid():
            error = serializer.errors
            serializer.save()
        else:
            validar_error = True
            error = serializer.errors

    def perform_update(self, serializer):
        if serializer.is_valid():
            error = serializer.errors
            serializer.save()
        else:
            validar_error = True
            error = serializer.errors

    def list(self, request):
        data = self.get_queryset()
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer_persona = self.serializer_class(data=request.data)
        serializer_persona.is_valid(raise_exception=True)
        self.perform_create(serializer_persona)
        return Response(serializer_persona.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        persona_data = self.get_queryset(kwargs['pk'])
        serializer_persona = PersonaDetalleSerializer(persona_data)
        return Response(serializer_persona.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        persona_data = self.get_queryset(kwargs['pk'])

        if not persona_data:
            return Response({'Error':'No existe este usuario con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_persona = self.serializer_class(persona_data, request.data)
        self.perform_update(serializer_persona)
        return Response(serializer_persona.data,{'mensaje':f'{self.model.__name__}Ha sido actualizado exitosamente!'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        persona = self.get_queryset(kwargs['pk'])

        if not persona:
            return Response({'Error':'No existe este usuario con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        persona.estado = False
        persona.save()
        return Response({'mensage':'el usuario ha sido eliminado!'},status=status.HTTP_204_NO_CONTENT)