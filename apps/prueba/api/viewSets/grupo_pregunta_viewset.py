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

    def crear_enunciados_pregunta(self, enunciados=[]):
        validar_errores = False
        enunciados_validos = []
        errores_enunciados = []

        for enunciado in enunciados:
            enunciado_pregunta_serializer = EnunciadoPreguntaSerializer(data = enunciado)
            if enunciado_pregunta_serializer.is_valid():
                enunciado_valido = EnunciadoPregunta(
                    enunciado = enunciado_pregunta_serializer.validated_data['enunciado'],
                    pregunta = enunciado_pregunta_serializer.validated_data['pregunta']
                )
                enunciados_validos.append(enunciado_valido)
                errores_enunciados.append(enunciado_pregunta_serializer.errors)
            else:
                validar_errores = True
                errores_enunciados.append(enunciado_pregunta_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'enunciados_validos': enunciados_validos,
            'errores_enunciados': errores_enunciados
        }

    def crear_opciones_pregunta(self, opciones=[]):
        validar_errores = False
        opciones_validas = []
        errores_opciones = []

        for opcion_pregunta in opciones:
            opciones_pregunta_serializer = OpcionPreguntaSerializer(data = opcion_pregunta)
            if opciones_pregunta_serializer.is_valid():
                opcion = OpcionPregunta(
                    contenido_opcion = opciones_pregunta_serializer.validated_data['contenido_opcion'],
                    pregunta = opciones_pregunta_serializer.validated_data['pregunta'],
                    letra = opciones_pregunta_serializer.validated_data['letra'],
                )
                opciones_validas.append(opcion)
                errores_opciones.append(opciones_pregunta_serializer.errors)
            else:
                validar_errores = True
                errores_opciones.append(opciones_pregunta_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'opciones_validas': opciones_validas,
            'errores_opciones': errores_opciones
        }

    def crear_enunciados_grupo_pregunta(self, enunciados_grupo_pregunta=[]):
        validar_errores = False
        enunciados_grupo_pregunta_validos = []
        errores_enunciados_grupo_pregunta = []

        for enunciado in enunciados_grupo_pregunta:
            enunciados_grupo_pregunta_serializer = EnunciadoGrupoPreguntaSerializer(data=enunciado)
            if enunciados_grupo_pregunta_serializer.is_valid():
                enunciado_valido = EnunciadoGrupoPregunta(
                    enunciado_general = enunciados_grupo_pregunta_serializer.validated_data['enunciado_general'],
                    grupo = enunciados_grupo_pregunta_serializer.validated_data['grupo']
                )
                enunciados_grupo_pregunta_validos.append(enunciado_valido)
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta.append(enunciados_grupo_pregunta_serializer.errors)

        return {
            'validar_errores':validar_errores,
            'enunciados_grupo_pregunta_validos': enunciados_grupo_pregunta_validos,
            'errores_enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta
        }

    def crear_justificacion_pregunta(self, justificacion={}):
        validar_errores = False
        errores_justificacion = []

        justificacion_serializer = JustificacionSerializer(data=justificacion)
        if justificacion_serializer.is_valid() != True:
            validar_errores = True
            errores_justificacion.append(justificacion_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'errores_justificacion': errores_justificacion,
            'justificacion': justificacion_serializer
        }

    def crear_pregunta(self, pregunta={}):
        validar_errores = False
        errores_pregunta = []
        pregunta_valida = {}

        pregunta_serializer = PreguntaSerializer(data=pregunta)
        if pregunta_serializer.is_valid():
            pregunta_valida = Pregunta(
                grupo = pregunta_serializer.validated_data['grupo'],
                respuesta = pregunta_serializer.validated_data['respuesta'],
                justificacion = pregunta_serializer.validated_data['justificacion']
            )
        else:
            validar_errores = True
            errores_pregunta.append(pregunta_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'errores_pregunta': errores_pregunta,
            'pregunta': pregunta_valida
        }

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
        justificaciones_creadas = []
        preguntas_validas, enunciados_pregunta_validas, opciones_pregunta_validas = {}, {}, {}
        enunciados_grupo_pregunta_validas = []
        (errores_grupo_pregunta, errores_enunciados_grupo_pregunta, errores_preguntas,
            errores_enunciados_pregunta, errores_opciones_pregunta, errores_justificacion, error) = [], [], [], [], [], [], {}

        grupo_preguntas = request.data['grupo_preguntas']
        enunciados_grupo_pregunta = request.data['enunciados_grupo_pregunta']
        preguntas = request.data['preguntas']

        grupo_preguntas_serializer = self.serializer_class(data = grupo_preguntas)

        if grupo_preguntas_serializer.is_valid():
            errores_grupo_pregunta = grupo_preguntas_serializer.errors
        else:
            validar_errores = True
            errores_grupo_pregunta = grupo_preguntas_serializer.errors

        errores_grupo_pregunta = {'grupo_preguntas': errores_grupo_pregunta}
        error.update(errores_grupo_pregunta)

        #Pregunta
        for indice, pregunta in enumerate(preguntas):
            #Valdiaciones para la justificación
            datos_justificacion = self.crear_justificacion_pregunta(pregunta['justificacion'])
            if datos_justificacion['validar_errores'] != True:
                datos_justificacion['justificacion'].save()
                justificaciones_creadas.append({id:datos_justificacion['justificacion'].data['id']})
                pregunta['justificacion_id'] = datos_justificacion['justificacion'].data['id']
            else:
                validar_errores: datos_justificacion['validar_errores']
                errores_justificacion.append({
                    'justificacion':datos_justificacion['errores_justificacion'],
                    'indice':indice
                })

            #validaciones para la pregunta
            datos_crear_pregunta = self.crear_pregunta(pregunta['pregunta'])
            if datos_crear_pregunta['validar_errores'] != True:
                preguntas_validas[indice] = datos_crear_pregunta['pregunta']
            else:
                validar_errores = True
                errores_preguntas.append({
                    'pregunta': datos_crear_pregunta['errores_pregunta'],
                    'indice': indice
                })

            # Validaciones para opciones de la pregunta
            datos_crear_opciones_pregunta = self.crear_opciones_pregunta(pregunta['opciones_pregunta'])
            if datos_crear_opciones_pregunta['validar_errores'] != True:
                opciones_pregunta_validas[indice] = datos_crear_opciones_pregunta['opciones_validas']
            else:
                validar_errores = True
                errores_opciones_pregunta.append({
                    'opciones': datos_crear_opciones_pregunta['errores_opciones'],
                    'inidice': indice
                })

            #Validaciones para enunciados de la pregunta
            # datos_crear_enunciado_pregunta = self.crear_enunciados_grupo_pregunta(pregunta['enunciados_pregunta'])
            # if datos_crear_enunciado_pregunta['validar_errores'] != True:
            #     enunciados_pregunta_validas[indice] = datos_crear_enunciado_pregunta['enunciados_validos']
            # else:
            #     validar_errores = True
            #     errores_enunciados_pregunta.append({
            #         'enunciados':datos_crear_enunciado_pregunta['errores_enunciados'],
            #         'indice': indice
            #     })

        errores_justificacion = {'justificacions': errores_justificacion}
        error.update(errores_justificacion)

        errores_pregunta = {'preguntas': errores_preguntas}
        error.update(errores_pregunta)

        errores_enunciados_pregunta = {'enunciados_pregunta': errores_enunciados_pregunta}
        error.update(errores_enunciados_pregunta)

        errores_opciones_pregunta = {'opciones_pregunta': errores_opciones_pregunta}
        error.update(errores_opciones_pregunta)

        #Enunciados grupo pregunta
        datos_crear_enuciados_grupo_pregunta = self.crear_enunciados_grupo_pregunta(enunciados_grupo_pregunta)
        if datos_crear_enuciados_grupo_pregunta['validar_errores'] != True:
            enunciados_grupo_pregunta_validas[indice] = datos_crear_enuciados_grupo_pregunta['enunciados_grupo_pregunta_validos']
        else:
            validar_errores = True
            errores_enunciados_grupo_pregunta.append(datos_crear_enuciados_grupo_pregunta['errores_enunciados_grupo_pregunta'])

        errores_enunciados_grupo_pregunta = {'enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta}
        error.update(errores_enunciados_grupo_pregunta)

        if validar_errores:
            return Response({'error':error}, status = status.HTTP_400_BAD_REQUEST)

        #Grupo Preguntas
        grupo_preguntas_serializer.save()
        datos_grupo = grupo_preguntas_serializer.data['id']

        for enunciado_grupo in enunciados_grupo_pregunta_validas:
            enunciado_grupo.grupo = datos_grupo

        EnunciadoGrupoPregunta.objects.bulk_create(enunciados_grupo_pregunta_validas)

        #Registro de preguntas
        for pregunta in preguntas_validas:
            pregunta['grupo'] = datos_grupo

        preguntas_creadas = Pregunta.objects.bulk_create(preguntas_validas)

        datos_enunciados = []
        for indice, pregunta in enumerate(preguntas_creadas):
            for enunciado in enunciados_pregunta_validas[indice]:
                enunciado['pregunta'] = pregunta
                datos_enunciados.append(enunciado)

        return Response({'mensaje':'Se ha registrado correctamente el grupo de preguntas'}, status = status.HTTP_201_CREATED)