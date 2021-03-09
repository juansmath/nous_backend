from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasSerializer, BancoPreguntasDetalleSerializer

from apps.prueba.models import BancoPreguntas

class BancoPreguntaViewSet(viewsets.ViewSet):
    model = BancoPreguntas
    serializer_class = BancoPreguntasSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.model.objects.filter(estado = True)
        else:
            return self.model.objects.filter(id = pk, estado = True)

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

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer_banco_pregunta = self.serializer_class(data = request.data)
        print(serializer_banco_pregunta)
        self.perform_create(serializer_banco_pregunta)
        return Response(serializer_banco_pregunta.data,{'mensaje':'El banco de preguntas se creo exitosamente!'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        data_banco_pregunta = self.get_queryset(kwargs['pk'])
        serializer_banco_pregunta = BancoPreguntasDetalleSerializer(data_banco_pregunta)
        return Response(serializer_banco_pregunta.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        data_banco_pregunta = self.get_queryset(kwargs['pk'])

        if not data_banco_pregunta:
            return Response({'mensaje':'No existe el banco de preguntas con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_banco_preguta = self.serializer_class(data_banco_pregunta, request.data)
        self.perform_update(serializer_banco_preguta)
        return Response(serializer_banco_preguta.data, {'mensaje':'El banco se ha actulizado correctamente!'}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        data_banco_pregunta = self.get_queryset(kwargs['pk'])

        if not data_banco_pregunta:
            return Response({'mensaje':'No existe un banco de preguntas con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(data_banco_pregunta)
        return Response({'mensaje':'El banco de preguntas ha sido eliminado!'}, status=status.HTTP_204_NO_CONTENT)