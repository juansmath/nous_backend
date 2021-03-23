import json
# from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
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
        data = PreguntaSerializer(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validar_errores = False
        opciones_pregunta_validas, enunciados_pregunta_validas = [], []
        errores_opciones, errores_justificacion, errores_enunciados, error_pregunta, error = {}, {}, {}, {}, {}

        pregunta = json.loads(request.data['pregunta'])

        justificacion_pregunta = pregunta['justificacion']
        enunciados_pregunta = pregunta['enunciados_pregunta']
        opciones_pregunta = pregunta['opciones_pregunta']

        del pregunta['justificacion']
        del pregunta['enunciados_pregunta']
        del pregunta['opciones_pregunta']

        data_pregunta = pregunta['pregunta']

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

        error.update(errores_justificacion)
        justificacion_serializer.save()
        data_pregunta['justificacion'] = justificacion_serializer.data

        pregunta_serializer = self.serializer_class(data = data_pregunta)
        if pregunta_serializer.is_valid():
            error_pregunta = pregunta_serializer.errors
        else:
            validar_errores = True
            error_pregunta = pregunta_serializer.errors

        error_pregunta = {'pregunta', error_pregunta}
        error.update(error_pregunta)

        for indice, enunciado in enumerate(enunciados_pregunta):
            enunciado_pregunta_serializer = EnunciadoPreguntaSerializer(data = enunciado)
            if enunciado_pregunta_serializer.is_valid():
                enunciado = EnunciadoPregunta(
                    enunciado = enunciado_pregunta_serializer.validated_data['enunciado'],
                    pregunta = enunciado_pregunta_serializer.validated_data['pregunta']
                )
                enunciados_pregunta_validas.append(enunciado)
                errores_enunciados[indice] = enunciado_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_enunciados[indice] = enunciado_pregunta_serializer.errors

        errores_enunciados = {'enunciado': errores_enunciados}
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
            justificacion = Justificacion.objects.filter(id = justificacion_serializer.data['id'])
            if justificacion:
                justificacion.delete()

        pregunta_serializer.save()
        pregunta = Pregunta.objects.filter(id = pregunta_serializer.data['id']).first()

        for enunciado in enunciados_pregunta_validas:
            enunciado.pregunta = pregunta

        for opcion in opciones_pregunta_validas:
            opcion.pregunta = pregunta

        EnunciadoPregunta.objects.bulk_create(enunciados_pregunta_validas)
        OpcionPregunta.objects.bulk_create(opciones_pregunta_validas)

        return Response({'mensaje':'Se ha registrado correctamente la pregunta'}, status = status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        validar_errores = False
        opciones_pregunta_validas, enunciados_pregunta_validas = [], []
        errores_opciones, errores_justificacion, errores_enunciados, error = {}, {}, {}, {}

        pregunta = json.loads(request.data['pregunta'])

        justificacion = pregunta['justificacion']
        opciones_pregunta = pregunta['opciones_pregunta']
        enunciados_pregunta = pregunta['enunciados_pregunta']

        del pregunta['justificacion']
        del pregunta['opciones_pregunta']
        del pregunta['enunciados_pregunta']

        data_pregunta = pregunta['pregunta']

        pregunta_actualizar = self.get_queryset(pk = kwargs['pk'])
        if not pregunta_actualizar:
            return Response({'error', 'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)

        pregunta_serializer = self.serializer_class(pregunta_actualizar, data = data_pregunta)

        if not pregunta_actualizar:
            error_pregunta = pregunta_serializer.errors
        else:
            validar_errores = True
            error_pregunta = pregunta_serializer.errors

        error_pregunta = {'pregunta', error_pregunta}
        error.update(error_pregunta)

        #Validación de justificacion
        data_justificacion = Justificacion.objects.filter(id = pregunta_serializer.data['justificacion']).first()
        if not data_justificacion:
            return Response({'error':'Esta Pregunta no tiene asociada ninguna justificación!'}, status=status.HTTP_400_BAD_REQUEST)

        justificacion_serializer = JustificacionSerializer(data_justificacion, justificacion)
        if justificacion_serializer.is_valid():
            errores_justificacion = justificacion_serializer.errors
        else:
            validar_errores = True
            errores_justificacion = justificacion_serializer.errors
            errores_justificacion = {'justificacion', error}

        error.update(errores_justificacion)

        #validación de los enunciados para la pregunta
        EnunciadoPregunta.objects.filter(pregunta = pregunta_actualizar.id).update(estado = False)

        for indice, enunciado in enumerate(enunciados_pregunta):
            enunciado_pregunta_serilizer = EnunciadoPreguntaSerializer(data = enunciado, context = data_pregunta.id)
            if enunciado_pregunta_serilizer.is_valid():
                EnunciadoPregunta.update_or_create(
                    enunciado = enunciado_pregunta_serilizer.validated_data['enunciado'],
                    pregunta = data_pregunta,
                    estado = True
                )
                errores_enunciados[indice] = enunciado_pregunta_serilizer.errors
            else:
                validar_errores = True
                errores_enunciados[indice] = enunciado_pregunta_serilizer.errors

        errores_enunciados = {'enunciados': errores_enunciados}
        error.update(errores_enunciados)
        EnunciadoPregunta.objects.filter(pregunta = kwargs['pk'], estado = False).delete()

        #validación de opciones para la pregunta
        OpcionPregunta.objects.filter(pregunta = data_pregunta.id).update(estado = False)

        for indice, opcion in enumerate(opciones_pregunta):
            opcion_pregunta_serializer = OpcionPreguntaSerializer(data = opcion, context = data_pregunta.id)
            if opcion_pregunta_serializer.is_valid():
                OpcionPregunta.update_or_create(
                    contenido_opcion = opcion_pregunta_serializer.validated_data['contenido_opcion'],
                    pregunta = data_pregunta,
                    letra = opcion_pregunta_serializer.validated_data['letra'],
                    estado = True
                )
                errores_opciones[indice] = opcion_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_opciones[indice] = opcion_pregunta_serializer.errors

        errores_opciones = {'opciones', errores_opciones}
        error.update(errores_opciones)
        OpcionPregunta.objects.filter(pregunta = data_pregunta.id, estado = False).delete()

        if validar_errores:
            return Response({'error': error}, estatus = status.HTTP_400_BAD_REQUEST)

        pregunta_serializer.update(pregunta_actualizar, pregunta_serializer.validated_data)

        return Response({'mensaje':'La pregunta se actualizada correctamente!'})

    def retrieve(self, request, format = None, pk = None):
        pregunta = Pregunta.objects.filter(id = self.kwargs['pk'], estado = True).first()
        if pregunta:
            data = PreguntaDetalleSerializer(pregunta)
            return Response(data.data, status = status.HTTP_200_OK)
        return Response({'error', 'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pregunta = self.get_queryset(pk = kwargs['pk'])

        if not pregunta:
            return Response({'error':'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            pregunta.delete()
            return Response({'mensaje':'La pregunta ha sido eliminada!'}, status = status.HTTP_200_OK)

