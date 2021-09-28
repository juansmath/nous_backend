from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasSerializer, BancoPreguntasDetalleSerializer

from apps.prueba.models import BancoPreguntas, Pregunta, GrupoPregunta

class BancoPreguntaViewSet(viewsets.ViewSet):
    model = BancoPreguntas
    serializer_class = BancoPreguntasSerializer

    def list(self, request):
        data = self.model.objects.filter(estado = True)
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        banco_pregunta_serializer = self.serializer_class(data = request.data)

        if banco_pregunta_serializer.is_valid():
            banco_pregunta_serializer.save()
            return Response({'mensaje':'El banco de preguntas se creo exitosamente!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos!', 'error': banco_pregunta_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        data_banco_pregunta = self.model.objects.filter(id = kwargs['pk'], estado = True).first()
        if not data_banco_pregunta:
            return Response({'mensaje':'No existe un banco de preguntas con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        serializer_banco_pregunta = BancoPreguntasDetalleSerializer(data_banco_pregunta)
        return Response(serializer_banco_pregunta.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        banco_pregunta = self.model.objects.filter(id = kwargs['pk'], estado = True)

        if not banco_pregunta:
            return Response({'mensaje':'No existe un banco de preguntas con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        banco_pregunta_serializer = self.serializer_class(banco_pregunta, request.data)
        if banco_pregunta_serializer.is_valid():
            banco_pregunta_serializer.update(banco_pregunta, request.data)
            return Response(banco_pregunta_serializer, {'mensaje':'El banco se ha actulizado correctamente!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos!', 'error': banco_pregunta_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        justificaciones = []

        banco_pregunta = self.model.objects.filter(id = kwargs['pk'], estado = True)

        if not banco_pregunta:
            return Response({'mensaje':'No existe un banco de preguntas con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        # preguntas = Pregunta.objects.filter(banco_pregunta = kwargs['pk'], estado = True).related_name("justificacion_id")
        # if preguntas:
        #     for pregunta in preguntas:
        #         pregunta.justificacion_id.delete()
        #         pregunta.delete();
                
        banco_pregunta.delete();

        return Response({'mensaje':'El banco de preguntas ha sido eliminado!'}, status=status.HTTP_200_OK)