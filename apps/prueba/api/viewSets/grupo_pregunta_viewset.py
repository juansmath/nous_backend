import json
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.grupo_pregunta_serializer import *
from apps.prueba.api.serializers.pregunta_serializer import *

from apps.prueba.models import (GrupoPregunta, EnunciadoGrupoPregunta,Pregunta, EnunciadoPregunta,
                                ImagenEnunciadoPregunta, Justificacion, OpcionPregunta)

class GrupoPreguntaViewSet(viewsets.ViewSet):
    model = GrupoPregunta
    serializer_class = GrupoPreguntaSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.model.objects.filter(estado = True)
        else:
            return self.model.objects.filter(id = pk, estado = True)

    def list(self, request):
        data = self.get_queryset()
        data = self.serializer_class(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request):
        validar_errores = False
        preguntas_validas, enunciados_pregunta_validas, opciones_pregunta_validas, enunciados_grupo_pregunta_validas = [], [], [], []
        (errores_grupo_pregunta, errores_enunciados_grupo_pregunta, errores_preguntas,
            errores_enunciados_pregunta, errores_opciones_pregunta, errores_justificacion, error) = {}, {}, {}, {}, {}, {}, {}

        grupo_preguntas = request.data['grupo_preguntas']
        enunciados_grupo_pregunta = grupo_preguntas['enunciados_grupo_pregunta']
        preguntas = grupo_preguntas['pregunta']

        preguntas = preguntas['pregunta']

        del grupo_preguntas['enunciados_grupo_pregunta']
        del grupo_preguntas['preguntas']

        data_grupo_pregunta = grupo_preguntas['grupo_preguntas']

        grupo_preguntas_serializer = self.serializer_class(data = data_grupo_pregunta)

        if grupo_preguntas_serializer.is_valid():
            errores_grupo_pregunta = grupo_preguntas_serializer.errors
        else:
            validar_errores = True
            errores_grupo_pregunta = grupo_preguntas_serializer.errors
        errores_grupo_pregunta = {'grupo_preguntas'}
        error.update(errores_grupo_pregunta)

        #Pregunta
        for indice, pregunta in enumerate(preguntas):
            justificacion = pregunta['justificacion']
            enunciados_pregunta = pregunta['enunciados_pregunta']
            opciones_pregunta = pregunta['opciones_pregunta']

            justificacion_serializer = JustificacionSerializer(data = justificacion)
            if justificacion_serializer.is_valid():
                errores_justificacion[indice] = justificacion_serializer.errors
            else:
                validar_errores = True
                errores_justificacion[indice] = justificacion_serializer.errores

            if validar_errores:
                errores_justificacion = {'justificacion': errores_justificacion}
                error.update(errores_justificacion)

            error.update(errores_justificacion)
            justificacion = {}

            justificacion_serializer.save()

            pregunta['pregunta']['justificacion'] = justificacion_serializer.data['id']
            pregunta_serializer = PreguntaSerializer(pregunta['pregunta'])

            if pregunta_serializer.is_valid():
                pregunta_individual = Pregunta(
                    grupo = pregunta_serializer.validated_data['grupo'],
                    respuesta = pregunta_serializer.validated_data['respuesta'],
                    justificacion = pregunta_serializer.validated_data['justificacion']
                )
                preguntas_validas.append(pregunta_individual)
                errores_pregunta[indice] = pregunta_serializer.errors
            else:
                validar_errores = True
                errores_preguntas[indice] = pregunta_serializer.errors

            #Enunciados pregunta
            for indice_enunciado, enunciado_pregunta in enumerate(enunciados_pregunta):
                enunciado_pregunta_serializer = EnunciadoPreguntaSerializer(data = enunciado_pregunta)
                if enunciado_pregunta_serializer.is_valid():
                    enunciado = EnunciadoPregunta(
                        enunciado = enunciado_pregunta_serializer.validated_data['enunciado'],
                        pregunta = enunciado_pregunta_serializer.validated_data['pregunta']
                    )
                    enunciados_pregunta_validas[indice].append(enunciado)
                    errores_enunciados_pregunta[indice_enunciado] = enunciado_pregunta_serializer.errors
                else:
                    validar_errores = True
                    errores_enunciados_pregunta[indice_enunciado] = enunciado_pregunta_serializer.errors

            errores_enunciados_pregunta[indice].append(errores_enunciados_pregunta)

            enunciados_pregunta = {}

            #Opciones pregunta
            for indice_opcion, opcion_pregunta in enumerate(opciones_pregunta):
                opcion_pregunta_serializer = OpcionPreguntaSerializer(data = opcion_pregunta)
                if opcion_pregunta_serializer.is_valid():
                    opcion = OpcionPregunta(
                        contenido_opcion = opcion_pregunta_serializer.validated_data['contenido_opcion'],
                        pregunta = opcion_pregunta_serializer.validated_data['pregunta'],
                        letra = opcion_pregunta_serializer.validated_data['letra'],
                    )
                    opciones_pregunta_validas[indice_opcion].append(opcion)
                    errores_opciones_pregunta[indice_opcion] = opcion_pregunta_serializer.errors
                else:
                    validar_errores = True
                    errores_opciones_pregunta[indice_opcion] = opcion_pregunta_serializer.errors

            errores_opciones_pregunta[indice].append(errores_opciones_pregunta)

            opciones_pregunta = {}

            if validar_errores:
                justificacion = Justificacion.objects.filter(id = justificacion_serializer.data['id'])
                if justificacion:
                    justificacion.delete()

        errores_pregunta = {'pregunta', errores_preguntas}
        error.update(errores_pregunta)

        errores_enunciados_pregunta = {'enunciados_pregunta', errores_enunciados_pregunta}
        error.update(errores_enunciados_pregunta)

        errores_opciones_pregunta = {'opciones_pregunta', errores_opciones_pregunta}
        error.update(errores_opciones_pregunta)

        for indice, enunciado_grupo in enumerate(enunciados_grupo_pregunta):
            enunciados_grupo_pregunta_serializer = EnunciadoGrupoPreguntaSerializer(data = enunciado_grupo)
            if enunciados_grupo_pregunta_serializer.is_valid():
                enunciado = EnunciadoGrupoPregunta(
                    enunciado_general = enunciados_grupo_pregunta_serializer.validated_data['enunciado_general'],
                    grupo_pregunta = enunciados_grupo_pregunta_serializer.validated_data['grupo_pregunta']
                )
                errores_enunciados_grupo_pregunta = enunciados_grupo_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta = enunciados_grupo_pregunta_serializer.errors

        errores_enunciados_grupo_pregunta = {'enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta}
        error.update(errores_enunciados_grupo_pregunta)

        if validar_errores:
            return Response({'error', error}, status = status.HTTP_400_BAD_REQUEST)

        #Grupo Preguntas
        grupo_preguntas_serializer.save()
        datos_grupo = GrupoPregunta.objects.filter(id = grupo_preguntas_serializer.data['id'])

        for enunciado_grupo in enunciados_grupo_pregunta_validas:
            enunciado_grupo.grupo = datos_grupo

        EnunciadoGrupoPregunta.objects.bulk_create(enunciados_grupo_pregunta_validas)

        #Guardando las preguntas
        for indice, pregunta in enumerate(preguntas_validas):
            pregunta.grupo = datos_grupo
            pregunta_serializer = PreguntaSerializer(pregunta)
            pregunta_serializer.save()

            datos_pregunta = Pregunta.objects.filter(id = pregunta_serializer.data['id']).first()

            #enunciados pregunta
            for enunciado in enunciados_pregunta_validas[indice]:
                enunciado.pregunta = datos_pregunta

            #opciones pregunta
            for opcion in opciones_pregunta_validas[indice]:
                opcion.pregunta = datos_pregunta

            EnunciadoPregunta.objects.bulk_create(enunciados_pregunta_validas)
            OpcionPregunta.objects.bulk_create(opciones_pregunta_validas)

            datos_pregunta = {}

        return Response({'mensaje':'Se ha registrado correctamente el grupo de preguntas'}, status = status.HTTP_201_CREATED)