from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasSerializer, BancoPreguntasDetalleSerializer

from apps.prueba.models import BancoPreguntas

class BancoPreguntaViewSet(viewsets.ViewSet):
    model = BancoPreguntas
    serializer_class = BancoPreguntasSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(args)
