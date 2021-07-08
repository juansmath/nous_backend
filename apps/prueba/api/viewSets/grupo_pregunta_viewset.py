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

        for opcion in opciones:
            opciones_pregunta_serializer = OpcionPreguntaSerializer(data = opcion)
            if opciones_pregunta_serializer.is_valid():
                opcion_valida = OpcionPregunta(
                    contenido_opcion = opciones_pregunta_serializer.validated_data['contenido_opcion'],
                    pregunta = opciones_pregunta_serializer.validated_data['pregunta'],
                    letra = opciones_pregunta_serializer.validated_data['letra'],
                )
                opciones_validas.append(opcion_valida)
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
        enunciados_grupo_pregunta_validas = []
        errores_enunciados_grupo_pregunta = []

        for indice, enunciado in enumerate(enunciados_grupo_pregunta):
            enunciados_grupo_pregunta_serializer = EnunciadoGrupoPreguntaSerializer(data=enunciado)
            if enunciados_grupo_pregunta_serializer.is_valid():
                enunciado_valido = EnunciadoGrupoPregunta(
                    enunciado_general = enunciados_grupo_pregunta_serializer.validated_data['enunciado_general'],
                    grupo = enunciados_grupo_pregunta_serializer.validated_data['grupo']
                )
                enunciados_grupo_pregunta_validas.append(enunciado_valido)
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta.append({
                    'enunciado': enunciados_grupo_pregunta_serializer.errors,
                    'indice': indice
                })

        return {
            'validar_errores':validar_errores,
            'enunciados_grupo_pregunta_validas': enunciados_grupo_pregunta_validas,
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
            'pregunta_valida': pregunta_valida
        }

    def crear_multiples_preguntas(self,preguntas=[]):
        validar_errores = False
        justificaciones_creadas = []
        preguntas_validas, enunciados_pregunta_validas, opciones_pregunta_validas = [], [], []
        errores_preguntas, errores_enunciados_pregunta, errores_opciones_pregunta, errores_justificacion = [], [], [], []

        for indice, pregunta in enumerate(preguntas):
            #Valdiaciones para la justificación
            datos_justificacion = self.crear_justificacion_pregunta(pregunta['justificacion'])
            if datos_justificacion['validar_errores'] != True:
                datos_justificacion['justificacion'].save()
                pregunta['pregunta']["justificacion"] = datos_justificacion['justificacion'].data['id']
                justificaciones_creadas.append({"id":datos_justificacion['justificacion'].data['id']})
            else:
                validar_errores: datos_justificacion['validar_errores']
                errores_justificacion.append({
                    'justificacion':datos_justificacion['errores_justificacion'],
                    'indice_pregunta':indice
                })

            #validaciones para la pregunta
            datos_crear_pregunta = self.crear_pregunta(pregunta['pregunta'])
            if datos_crear_pregunta['validar_errores'] != True:
                preguntas_validas.append(datos_crear_pregunta['pregunta_valida'])
            else:
                validar_errores = True
                errores_preguntas.append(datos_crear_pregunta['errores_pregunta'])

            # Validaciones para opciones de la pregunta
            datos_crear_opciones_pregunta = self.crear_opciones_pregunta(pregunta['opciones_pregunta'])
            if datos_crear_opciones_pregunta['validar_errores'] != True:
                opciones_pregunta_validas.append({
                    'opciones': datos_crear_opciones_pregunta['opciones_validas'],
                    'indice_pregunta': indice
                })
            else:
                validar_errores = True
                errores_opciones_pregunta.append({
                    'opciones': datos_crear_opciones_pregunta['errores_opciones'],
                    'indice_pregunta': indice
                })

            #Validaciones para enunciados de la pregunta
            datos_crear_enunciado_pregunta = self.crear_enunciados_pregunta(pregunta['enunciados_pregunta'])
            if datos_crear_enunciado_pregunta['validar_errores'] != True:
                enunciados_pregunta_validas.append({
                    'enunciados': datos_crear_enunciado_pregunta['enunciados_validos'],
                    'indice_pregunta': indice
                })
            else:
                validar_errores = True
                errores_enunciados_pregunta.append({
                    'enunciados':datos_crear_enunciado_pregunta['errores_enunciados'],
                    'indice_pregunta': indice
                })

        return {
            'validar_errores': validar_errores,
            'justificaciones_creadas': justificaciones_creadas,
            'preguntas_validas': preguntas_validas,
            'enunciados_pregunta_validas': enunciados_pregunta_validas,
            'opciones_pregunta_validas': opciones_pregunta_validas,
            'errores_preguntas': errores_preguntas,
            'errores_enunciados_pregunta': errores_enunciados_pregunta,
            'errores_opciones_pregunta': errores_opciones_pregunta,
            'errores_justificacion': errores_justificacion
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
        (preguntas_validas, enunciados_pregunta_validas, opciones_pregunta_validas,
            enunciados_grupo_pregunta_validas) = [], [], [], []
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

        #Preguntas
        if len(preguntas) != 0:
            datos_preguntas = self.crear_multiples_preguntas(preguntas)
            preguntas_validas = datos_preguntas['preguntas_validas']
            opciones_pregunta_validas = datos_preguntas['opciones_pregunta_validas']
            enunciados_pregunta_validas = datos_preguntas['enunciados_pregunta_validas']
            justificaciones_creadas = datos_preguntas['justificaciones_creadas']

            validar_errores = datos_preguntas['validar_errores']
            errores_preguntas = datos_preguntas['errores_preguntas']
            errores_enunciados_pregunta = datos_preguntas['errores_enunciados_pregunta']
            errores_opciones_pregunta = datos_preguntas['errores_opciones_pregunta']
            errores_justificacion = datos_preguntas['errores_justificacion']

        errores_justificacion = {'justificacions': errores_justificacion}
        error.update(errores_justificacion)

        errores_preguntas = {'preguntas': errores_preguntas}
        error.update(errores_preguntas)

        errores_enunciados_pregunta = {'enunciados_pregunta': errores_enunciados_pregunta}
        error.update(errores_enunciados_pregunta)

        errores_opciones_pregunta = {'opciones_pregunta': errores_opciones_pregunta}
        error.update(errores_opciones_pregunta)

        #Enunciados grupo pregunta
        if len(enunciados_grupo_pregunta) != 0:
            datos_crear_enuciados_grupo_pregunta = self.crear_enunciados_grupo_pregunta(enunciados_grupo_pregunta)
            if datos_crear_enuciados_grupo_pregunta['validar_errores'] != True:
                enunciados_grupo_pregunta_validas = datos_crear_enuciados_grupo_pregunta['enunciados_grupo_pregunta_validas']
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta = datos_crear_enuciados_grupo_pregunta['errores_enunciados_grupo_pregunta']

        errores_enunciados_grupo_pregunta = {'enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta}
        error.update(errores_enunciados_grupo_pregunta)

        # validar_errores = True
        if validar_errores:
            for justificacion in justificaciones_creadas:
                Justificacion.objects.filter(id = justificacion['id']).delete()

            return Response({'error':error}, status = status.HTTP_400_BAD_REQUEST)

        #Grupo Preguntas
        grupo_preguntas_serializer.save()
        grupo = GrupoPregunta.objects.filter(id = grupo_preguntas_serializer.data['id']).first()

        for enunciado_grupo in enunciados_grupo_pregunta_validas:
            enunciado_grupo.grupo = grupo

        EnunciadoGrupoPregunta.objects.bulk_create(enunciados_grupo_pregunta_validas)

        #Registro de preguntas
        for pregunta in preguntas_validas:
            pregunta.grupo = grupo

        preguntas_creadas = Pregunta.objects.bulk_create(preguntas_validas)

        #Registro masivo de enunciados pregunta
        datos_enunciados = []
        for indice, pregunta in enumerate(preguntas_creadas):
            if enunciados_pregunta_validas[indice]['indice_pregunta'] == indice:
                for enunciado in enunciados_pregunta_validas[indice]['enunciados']:
                    enunciado.pregunta = pregunta
                    datos_enunciados.append(enunciado)

        EnunciadoPregunta.objects.bulk_create(datos_enunciados)

        datos_opciones = []
        for indice, pregunta in enumerate(preguntas_creadas):
            if opciones_pregunta_validas[indice]['indice_pregunta'] == indice:
                for opcion in opciones_pregunta_validas[indice]['opciones']:
                    opcion.pregunta = pregunta
                    datos_opciones.append(opcion)

        OpcionPregunta.objects.bulk_create(datos_opciones)

        return Response({'mensaje':'Se ha registrado correctamente el grupo de preguntas'}, status = status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        validar_errores = False

        (justificaciones_creadas, preguntas_validas, enunciados_pregunta_validas,
            enunciados_pregunta_validas_nuevas, opciones_pregunta_validas,
            opciones_pregunta_validas_nuevas, enunciados_grupo_pregunta_validas) = [], [], [], [], [], [], []

        (errores_grupo_pregunta, errores_enunciados_grupo_pregunta, errores_preguntas,
            errores_enunciados_pregunta, errores_enunciados_pregunta_editar, errores_opciones_pregunta,
            errores_opciones_pregunta_editar, errores_justificacion, error) = [], [], [], [], [], [], [], [], {}

        grupo_preguntas = request.data['grupo_preguntas']
        enunciados_grupo_pregunta = request.data['enunciados_grupo_pregunta']
        enunciados_grupo_pregunta_editar = request.data['enunciados_grupo_pregunta_editar']
        enunciados_grupo_pregunta_borrar = request.data['enunciados_grupo_pregunta_borrar']

        preguntas = request.data['preguntas']
        preguntas_editar = request.data['preguntas_editar']
        preguntas_borrar = request.data['preguntas_borrar']
        enunciados_pregunta_nuevas = request.data['enunciados_pregunta_nuevas']
        enunciados_pregunta_editar = request.data['enunciados_pregunta_editar']
        enunciados_pregunta_borrar = request.data['enunciados_pregunta_borrar']
        opciones_pregunta_nuevas = request.data['opciones_pregunta_nuevas']
        opciones_pregunta_editar = request.data['opciones_pregunta_editar']
        opciones_pregunta_borrar = request.data['opciones_pregunta_borrar']

        justificaciones_editar = request.data['justificaciones_editar']

        datos_grupo_pregunta = GrupoPregunta.objects.filter(id = kwargs['pk']).first()
        if not datos_grupo_pregunta:
            return Response({'error', 'No existe un grupo de preguntas con los datos proporcionados!'}, status = status.HTTP_400_BAD_REQUEST)

        grupo_preguntas_serializer = self.serializer_class(datos_grupo_pregunta, grupo_preguntas)

        if grupo_preguntas_serializer.is_valid() != True:
            validar_errores = True
            errores_grupo_pregunta.append(grupo_preguntas_serializer.errors)

        errores_grupo_pregunta = {'grupo_preguntas': errores_grupo_pregunta}
        error.update(errores_grupo_pregunta)

        if len(enunciados_grupo_pregunta) != 0:
            datos_crear_enuciados_grupo_pregunta = self.crear_enunciados_grupo_pregunta(enunciados_grupo_pregunta)
            if datos_crear_enuciados_grupo_pregunta['validar_errores'] != True:
                enunciados_grupo_pregunta_validas = datos_crear_enuciados_grupo_pregunta['enunciados_grupo_pregunta_validas']
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta = datos_crear_enuciados_grupo_pregunta['errores_enunciados_grupo_pregunta']

        errores_enunciados_grupo_pregunta = {'enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta}
        error.update(errores_enunciados_grupo_pregunta)

        #Edición de grupo de enunciados
        if len(enunciados_grupo_pregunta_editar) != 0:
            for indice, enunciado in enumerate(enunciados_grupo_pregunta_editar):
                datos_enunciado = EnunciadoGrupoPregunta.objects.filter(id = enunciado['id']).first()
                enunciados_grupo_pregunta_serializer = EnunciadoGrupoPreguntaSerializer(datos_enunciado, enunciado)
                if enunciados_grupo_pregunta_serializer.is_valid():
                    enunciados_grupo_pregunta_serializer.update(datos_enunciado, enunciado)
                else:
                    validar_errores = True
                    errores_enunciados_grupo_pregunta.append({
                        'enunciado': enunciados_grupo_pregunta_serializer.errors,
                        'indice': indice
                    })

        #Creacion de grupo de enunciados
        if len(enunciados_grupo_pregunta) != 0:
            datos_crear_enuciados_grupo_pregunta = self.crear_enunciados_grupo_pregunta(enunciados_grupo_pregunta)
            if datos_crear_enuciados_grupo_pregunta['validar_errores'] != True:
                enunciados_grupo_pregunta_validas = datos_crear_enuciados_grupo_pregunta['enunciados_grupo_pregunta_validas']
            else:
                validar_errores = True
                errores_enunciados_grupo_pregunta = datos_crear_enuciados_grupo_pregunta['errores_enunciados_grupo_pregunta']

        errores_enunciados_grupo_pregunta = {'enunciados_grupo_pregunta': errores_enunciados_grupo_pregunta}
        error.update(errores_enunciados_grupo_pregunta)

        #Edición de justificaciones
        if len(justificaciones_editar) != 0:
            for justificacion in justificaciones_editar:
                datos_justificacion = Justificacion.objects.fliter(id = justificacion['id']).first()
                justificacion_serializer = JustificacionSerializer(datos_justificacion, justificacion)
                if justificacion_serializer.is_valid():
                    justificacion_serializer.update(datos_justificacion, justificacion)
                else:
                    validar_errores = True
                    errores_justificacion.append({
                        'justificacion': justificacion_serializer.errors,
                        'indice_pregunta': justificacion['indice_pregunta']
                    })

        #Edición de Preguntas
        if len(preguntas_editar) != 0:
            for pregunta in preguntas_editar:
                datos_pregunta = Pregunta.objects.filter(id = pregunta['id']).first()
                pregunta_serialiazer = PreguntaSerializer(datos_pregunta, pregunta)
                if pregunta_serialiazer.is_valid():
                    pregunta_serialiazer.update(datos_pregunta, pregunta)
                else:
                    validar_errores = True
                    errores_preguntas.append({
                        'pregunta': pregunta_serialiazer.errors,
                        'indice_pregunta': pregunta['indice_pregunta']
                    })

        if len(preguntas) != 0:
            datos_preguntas = self.crear_multiples_preguntas(preguntas)
            preguntas_validas = datos_preguntas['preguntas_validas']
            opciones_pregunta_validas = datos_preguntas['opciones_pregunta_validas']
            enunciados_pregunta_validas = datos_preguntas['enunciados_pregunta_validas']
            justificaciones_creadas = datos_preguntas['justificaciones_creadas']

            validar_errores = datos_preguntas['validar_errores']
            errores_preguntas = datos_preguntas['errores_preguntas']
            errores_enunciados_pregunta = datos_preguntas['errores_enunciados_pregunta']
            errores_opciones_pregunta = datos_preguntas['errores_opciones_pregunta']
            errores_justificacion = datos_preguntas['errores_justificacion']

        #Edición de opciones pregunta
        if len(opciones_pregunta_editar) != 0:
            for opcion in opciones_pregunta_editar:
                datos_opcion = OpcionPregunta.objects.filter(id = opcion['id']).first()
                opcion_pregunta_serializer = OpcionPreguntaSerializer(datos_opcion, opcion)
                if opcion_pregunta_serializer.is_valid():
                    opcion_pregunta_serializer.update(datos_opcion, opcion)
                else:
                    validar_errores = True
                    errores_opciones_pregunta_editar.append({
                        'indice_pregunta': opcion['indice_pregunta'],
                        'indice_opcion': opcion['indice_opcion'],
                        'error_opcion_editar': opcion_pregunta_serializer.errors
                    })

        if len(opciones_pregunta_nuevas) != 0:
            for opcion in opciones_pregunta_nuevas:
                datos_opciones = self.crear_opciones_pregunta(opcion['opciones_pregunta'])
                if datos_opciones['validar_errores'] != True:
                    opciones_pregunta_validas_nuevas.append({
                        'pregunta_id': opcion["pregunta_id"],
                        'opciones_validas': datos_opciones['opciones_validas']
                    })
                else:
                    validar_errores = datos_opciones['validar_errores']
                    errores_opciones_pregunta.append({
                        'opciones': datos_opciones['errores_opciones'],
                        'indice_pregunta': opcion['indice_pregunta']
                    })