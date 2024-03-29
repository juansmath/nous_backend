import json
# from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.pregunta_serializer import *

from apps.prueba.models import (Pregunta, EnunciadoPregunta, ImagenEnunciadoPregunta, Justificacion,
                                OpcionPregunta, NivelEjecucion, OpcionesLetras, BancoPreguntas, NivelDificultad,
                                Modulo, Competencia)

class PreguntaViewSet(viewsets.ViewSet):
    model = Pregunta
    serializer_class = PreguntaSerializer

    def get_queryset(self, pk = None):
        if pk is None:
            return self.model.objects.filter(estado = True)
        else:
            return self.model.objects.filter(id = pk, estado = True).first()

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
            else:
                validar_errores = True
                errores_opciones.append(opciones_pregunta_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'opciones_validas': opciones_validas,
            'errores_opciones': errores_opciones
        }

    def obtener_nivel_ejecucion(self, modulo=None, nivel_dificultad=None):
        return NivelEjecucion.objects.get(modulo=modulo, nivel_dificultad=nivel_dificultad, estado=True)

    def obtener_preguntas_registradas(self, banco_preguntas='', nivel_dificultad=''):
        return Pregunta.objects.filter(banco_preguntas=banco_preguntas, nivel_dificultad=nivel_dificultad, estado=True)

    def calcular_valor_pregunta(self, cantidad_preguntas=0, puntaje_maximo=0):
        return puntaje_maximo/(cantidad_preguntas)

    def actualizar_valor_preguntas(self, preguntas, valor_pregunta):
        for pregunta in preguntas:
            pregunta.valor_pregunta = valor_pregunta

        Pregunta.objects.bulk_update(preguntas, ['valor_pregunta'])

    def actualizar_preguntas(self, banco_preguntas_id, nivel_dificultad_id, modulo_id, nueva=False):
        valor_pregunta = 0
        banco_preguntas = self.obtener_preguntas_registradas(banco_preguntas_id, nivel_dificultad_id)
        cantidad_preguntas = len(banco_preguntas)
        nivel_ejecucion = self.obtener_nivel_ejecucion(modulo_id, nivel_dificultad_id)

        if nueva:
            if cantidad_preguntas > 0:
                valor_pregunta = self.calcular_valor_pregunta(cantidad_preguntas, nivel_ejecucion.puntaje_maximo)
            else:
                valor_pregunta = self.calcular_valor_pregunta(cantidad_preguntas+1, nivel_ejecucion.puntaje_maximo)

        self.actualizar_valor_preguntas(banco_preguntas, valor_pregunta)

        return valor_pregunta

    def list(self, request):
        data = self.get_queryset()
        data = PreguntaSerializer(data, many = True)
        return Response(data.data, status = status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        validar_errores = False
        opciones_pregunta_validas, enunciados_pregunta_validas = [], []
        errores_opciones, errores_justificacion, errores_enunciados, error_pregunta, error = [], [], [], [], {}

        pregunta = request.data['pregunta']

        justificacion_pregunta = request.data['justificacion']
        enunciados_pregunta = request.data['enunciados_pregunta']
        opciones_pregunta = request.data['opciones_pregunta']

        justificacion_serializer = JustificacionSerializer(data = justificacion_pregunta)
        if justificacion_serializer.is_valid() != True:
            validar_errores = True
            errores_justificacion.append(justificacion_serializer.errors)

        if validar_errores:
            errores_justificacion = {'justificacion': errores_justificacion}
            error.update(errores_justificacion)
            return Response({'error': error}, status = status.HTTP_400_BAD_REQUEST)

        error.update(errores_justificacion)
        justificacion_serializer.save()
        pregunta['justificacion_id'] = justificacion_serializer.data['id']

        pregunta_serializer = self.serializer_class(data = pregunta)
        if pregunta_serializer.is_valid() != True:
            validar_errores = True
            error_pregunta.append(pregunta_serializer.errors)

        error_pregunta = {'pregunta': error_pregunta}
        error.update(error_pregunta)

        #Creación de enunciados de acuerdo a la pregunta
        if len(enunciados_pregunta) != 0:
            datos_enunciado = self.crear_enunciados_pregunta(enunciados_pregunta)
            errores_enunciados = datos_enunciado['errores_enunciados']
            validar_errores = datos_enunciado['validar_errores']
            enunciados_pregunta_validas = datos_enunciado['enunciados_validos']

        errores_enunciados = {'enunciados': errores_enunciados}
        error.update(errores_enunciados)

        #Creación de opciones para la pregunta
        if len(opciones_pregunta) != 0:
            datos_opcion = self.crear_opciones_pregunta(opciones_pregunta)
            validar_errores = datos_opcion['validar_errores']
            errores_opciones = datos_opcion['errores_opciones']
            opciones_pregunta_validas = datos_opcion['opciones_validas']

        errores_opciones = {'opciones': errores_opciones}
        error.update(errores_opciones)

        if validar_errores:
            justificacion = Justificacion.objects.filter(id = justificacion_serializer.data['id']).delete()
            return Response({'error':error}, status=status.HTTP_400_BAD_REQUEST)

        modulo_id = pregunta['modulo_id']
        banco_preguntas_id = pregunta['banco_preguntas_id']
        nivel_dificultad_id = pregunta['nivel_dificultad_id']

        pregunta_serializer.validated_data['valor_pregunta'] = self.actualizar_preguntas(banco_preguntas_id, nivel_dificultad_id, modulo_id, True)

        pregunta_serializer.save()
        pregunta = self.get_queryset(pk=pregunta_serializer.data['id'])

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
        errores_opciones, errores_opciones_editar, errores_justificacion, errores_enunciados, errores_enunciados_editar, error_pregunta, error = [], [], [], [], [], [], {}
        datos_pregunta, datos_justificacion = {},{}

        pregunta_actualizada = request.data['pregunta']
        justificacion = request.data['justificacion']
        editar_justificacion = request.data["editar_justificacion"]
        opciones_pregunta = request.data['opciones_pregunta']
        opciones_pregunta_editar = request.data['opciones_pregunta_editar']
        opciones_pregunta_borrar = request.data['opciones_pregunta_borrar']
        enunciados_pregunta = request.data['enunciados_pregunta']
        enunciados_pregunta_editar = request.data['enunciados_pregunta_editar']
        enunciados_pregunta_borrar = request.data['enunciados_pregunta_borrar']

        datos_pregunta = self.model.objects.select_related('justificacion',
                                                           'respuesta',
                                                           'banco_preguntas',
                                                           'nivel_dificultad',
                                                           'modulo',
                                                           'competencia').get(id = kwargs['pk'])

        datos_justificacion = datos_pregunta.justificacion
        datos_respuesta = datos_pregunta.respuesta
        datos_banco_preguntas = datos_pregunta.banco_preguntas
        datos_nivel_dificultad = datos_pregunta.nivel_dificultad
        datos_competencia = datos_pregunta.competencia
        datos_modulo = datos_pregunta.modulo

        if not datos_pregunta:
            return Response({'mensaje':'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)

        banco_preguntas_id = pregunta_actualizada['banco_preguntas_id']
        nivel_dificultad_id = pregunta_actualizada['nivel_dificultad_id']
        respuesta_id = pregunta_actualizada['respuesta_id']
        modulo_id = pregunta_actualizada['modulo_id']
        competencia_id = pregunta_actualizada['competencia_id']

        if nivel_dificultad_id != datos_nivel_dificultad.id and banco_preguntas_id != datos_banco_preguntas.id:
            #Actualizar el valor de las preguntas nuevas
            valor_pregunta = self.actualizar_preguntas(banco_preguntas_id, nivel_dificultad_id, modulo_id, True)
            pregunta_actualizada['valor_pregunta'] = valor_pregunta

            #Actualizar valores de otras preguntas
            self.actualizar_preguntas(datos_banco_preguntas.id, datos_nivel_dificultad.id, modulo_id)

        elif nivel_dificultad_id == datos_nivel_dificultad.id and banco_preguntas_id != datos_banco_preguntas.id:
            #Actualizar el valor de las preguntas nuevas
            valor_pregunta = self.actualizar_preguntas(banco_preguntas_id, nivel_dificultad_id, modulo_id, True)
            pregunta_actualizada['valor_pregunta'] = valor_pregunta

            #Actualizar valores de otras preguntas
            self.actualizar_preguntas(datos_banco_preguntas.id, nivel_dificultad_id, modulo_id)

        elif nivel_dificultad_id != datos_nivel_dificultad.id and banco_preguntas_id == datos_banco_preguntas.id:
            #Actualizar el valor de las preguntas nuevas
            valor_pregunta = self.actualizar_preguntas(banco_preguntas_id, nivel_dificultad_id, modulo_id, True)
            pregunta_actualizada['valor_pregunta'] = valor_pregunta

            #Actualizar valores de otras preguntas
            self.actualizar_preguntas(banco_preguntas_id, datos_nivel_dificultad.id, modulo_id)
        else:
            pregunta_actualizada['nivel_dificultad_id'] = datos_nivel_dificultad.id
            pregunta_actualizada['banco_preguntas_id'] = datos_banco_preguntas.id

        #Validación de justificacion
        if editar_justificacion:
            justificacion_serializer = JustificacionSerializer(datos_justificacion, justificacion)
            if justificacion_serializer.is_valid():
                justificacion_serializer.update(datos_justificacion, justificacion)
            else:
                validar_errores = True
                errores_justificacion.append(justificacion_serializer.errors)

        errores_justificacion = {'justificacion': errores_justificacion}
        error.update(errores_justificacion)

        pregunta_serializer = self.serializer_class(datos_pregunta, pregunta_actualizada)

        if pregunta_serializer.is_valid() != True:
            validar_errores = True
            error_pregunta.append(pregunta_serializer.errors)

        error_pregunta = {'pregunta': error_pregunta}
        error.update(error_pregunta)

        #validación de los enunciados para la pregunta
        if len(enunciados_pregunta) != 0:
            datos_enunciado = self.crear_enunciados_pregunta(enunciados_pregunta)
            errores_enunciados = datos_enunciado['errores_enunciados']
            validar_errores = datos_enunciado['validar_errores']
            enunciados_pregunta_validas = datos_enunciado['enunciados_validos']

        errores_enunciados = {'enunciados': errores_enunciados}
        error.update(errores_enunciados)

        if len(enunciados_pregunta_editar) != 0:
            for indice, enunciado in enumerate(enunciados_pregunta_editar):
                datos_enunciado = EnunciadoPregunta.objects.filter(id = enunciado['id']).first()
                enunciado_pregunta_serializer = EnunciadoPreguntaSerializer(datos_enunciado, enunciado)
                if enunciado_pregunta_serializer.is_valid():
                    enunciado_pregunta_serializer.update(datos_enunciado, enunciado)
                else:
                    validar_errores = True
                    errores_enunciados_editar.append(enunciado_pregunta_serializer.errors)

        errores_enunciados_editar = {'enunciados_editar': errores_enunciados_editar}
        error.update(errores_enunciados_editar)

        #validación de opciones para la pregunta
        if len(opciones_pregunta) != 0:
            datos_opcion = self.crear_opciones_pregunta(opciones_pregunta)
            validar_errores = datos_opcion['validar_errores']
            errores_opciones = datos_opcion['errores_opciones']
            opciones_pregunta_validas = datos_opcion['opciones_validas']

        errores_opciones = {'opciones': errores_opciones}
        error.update(errores_opciones)

        if len(opciones_pregunta_editar) != 0:
            for indice, opcion in enumerate(opciones_pregunta_editar):
                datos_opcion = OpcionPregunta.objetcs.filter(id = opcion['id']).first()
                opcion_pregunta_serializer = OpcionPreguntaSerializer(datos_opcion, opcion)
                if opcion_pregunta_serializer.is_valid():
                    opcion_pregunta_serializer.update(datos_opcion, opcion)
                else:
                    validar_errores = True
                    errores_opciones_editar.append(opcion_pregunta_serializer.errors)

        errores_opciones_editar = {'opciones_editar': errores_opciones_editar}
        error.update(errores_opciones_editar)

        if validar_errores:
            return Response({'mensaje':'Ha ocurrido un error al actualizar la pregunta','error': error}, status = status.HTTP_400_BAD_REQUEST)

        if len(enunciados_pregunta_borrar) != 0:
            for enunciado in enunciados_pregunta_borrar:
                EnunciadoPregunta.objects.filter(id = enunciado['id']).delete()

        if len(opciones_pregunta_borrar) != 0:
            for opcion in opciones_pregunta_borrar:
                OpcionPregunta.objects.filter(id=opcion['id']).delete()

        pregunta_serializer.update(datos_pregunta, pregunta_actualizada)

        for enunciado in enunciados_pregunta_validas:
            enunciado.pregunta = datos_pregunta

        for opcion in opciones_pregunta_validas:
            opcion.pregunta = datos_pregunta

        EnunciadoPregunta.objects.bulk_create(enunciados_pregunta_validas)
        OpcionPregunta.objects.bulk_create(opciones_pregunta_validas)

        return Response({'mensaje':'La pregunta se ha actualizado correctamente!'}, status = status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        pregunta = Pregunta.objects.filter(id = kwargs['pk'], estado = True).first()
        if pregunta:
            data = PreguntaDetalleSerializer(pregunta)
            return Response(data.data, status = status.HTTP_200_OK)
        return Response({'error': 'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pregunta = Pregunta.objects.filter(id = kwargs['pk']).first()

        if not pregunta:
            return Response({'error':'No existe una pregunta con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)
        else:
            Justificacion.objects.filter(id = pregunta.justificacion_id).delete()
            pregunta.delete()
            return Response({'mensaje':'La pregunta ha sido eliminada!'}, status = status.HTTP_200_OK)

