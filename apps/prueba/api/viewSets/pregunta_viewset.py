from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.pregunta_serializer import *

from apps.prueba.models import Pregunta, EnunciadoPregunta, ImagenEnunciadoPregunta, Justificacion, OpcionPregunta

class PreguntaViewSet(viewsets.ViewSet):
    model = Pregunta
    serializer_class = PreguntaSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.model.objects.filter(estado = True)
        else:
            return self.model.objects.filter(id = pk, estado = True)

    def perform_destroy(self, instance):
        instance.delete()

    def list(self, request):
        data = self.get_queryset()
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validar_errores = False
        opciones_pregunta_validas, enunciados_pregunta_validos = [], []
        errores_opciones, errores_justificacion, errores_enunciados, error = {}, {}, {}, {}

        pregunta = request.data['pregunta']

        justificacion_pregunta = pregunta['justificacion']
        enunciados_pregunta = pregunta['enunciados_pregunta']
        opciones_pregunta = pregunta['opciones_pregunta']

        del pregunta['justificacion']
        del pregunta['enunciados_pregunta']
        del pregunta['opciones_pregunta']

        pregunta_data = pregunta['pregunta']

        justificacion_serializer = JustificacionSerializer(data = justificacion_pregunta)
        if justificacion_serializer.is_valid():
            errores_justificacion = justificacion_serializer.errors
        else:
            validar_errores = True
            errores_justificacion = justificacion_serializer.errors

        if validar_errores:
            errores_justificacion = {'justificacion': errores_justificacion}
            error.update(errores_justificacion)
            return Response({'error': error}, status = status.HTTP_400_BAD_REQUEST)

        justificacion_serializer.save()
        pregunta_data['justificacion'] = justificacion_serializer.data['id']

        pregunta_serializer = self.serializer_class(data = pregunta_data)
        if pregunta_serializer.is_valid():
            error = pregunta_serializer.errors
        else:
            validar_errores = True
            error = pregunta_serializer.errors
        print(pregunta_data)
        for indice, enunciado in enumerate(enunciados_pregunta):
            enunciado_pregunta_serializer = EnunciadoPreguntaSerializer(data = enunciado)
            if enunciado_pregunta_serializer.is_valid():
                enunciado = EnunciadoPregunta(
                    enunciado = enunciado_pregunta_serializer.validated_data['enunciado'],
                    pregunta = enunciado_pregunta_serializer.validated_data['pregunta']
                )
                enunciados_pregunta_validos.append(enunciado)
                errores_enunciados[indice] = enunciado_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_enunciados[indice] = enunciado_pregunta_serializer.errors

        errores_enunciados[indice] = {'enunciado': errores_enunciados}
        error.update(errores_enunciados)

        for indice, opcion_pregunta in enumerate(opciones_pregunta):
            opciones_pregunta_serializer = OpcionPreguntaSerializer(data = opcion_pregunta)
            if opciones_pregunta_serializer.is_valid():
                opcion = OpcionPregunta(
                    contenido_opcion = opciones_pregunta_serializer.validated_data['contenido_opcion'],
                    pregunta = opciones_pregunta_serializer.validated_data['pregunta'],
                    letra = opciones_pregunta_serializer.validated_data['letra'],
                )
                opciones_pregunta_validas.append(opcion)
                errores_opciones[indice] = opciones_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_opciones[indice] = opciones_pregunta_serializer.errors
        errores_opciones = {'opciones': errores_opciones}
        error.update(errores_opciones)

        if validar_errores:
            return Response({'error': error}, status = status.HTTP_400_BAD_REQUEST)

        pregunta_serializer.save()

        for enunciado in opciones_pregunta_validas:
            enunciado.pregunta = pregunta_serializer.data['id']

        for opcion in opciones_pregunta_validas:
            opcion.pregunta = pregunta_serializer.data['id']
            print('Hola---------------------------------------------')

        EnunciadoPregunta.objects.bulk_create(enunciados_pregunta_validos)
        OpcionPregunta.objects.bulk_create(opciones_pregunta_validas)

        return Response({'mensaje':'Se ha creado correctamente la pregunta'}, status = status.HTTP_201_CREATED)

