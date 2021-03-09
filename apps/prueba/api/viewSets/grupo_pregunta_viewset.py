from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.grupo_pregunta_serializer import *
from apps.prueba.api.serializers.pregunta_serializer import *

from apps.prueba.models import GrupoPregunta, EnunciadoGrupoPregunta

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
        preguntas_validas, enuciados_grupo_pregunta_valida, enunciado_pregunta_valida, opciones_pregunta_validas = [], [], [], []
        errores_pregunta, errores_enunciado_grupo_pregunta, errores_enunciado_pregunta, errores_opciones_pregunta, errores_justificacion = {}, {}, {}, {}, {}

        grupo_preguntas = request.data['grupo_pregunta']
        enunciados_grupo_pregunta = grupo_preguntas['enunciados_grupo_pregunta']
        preguntas = grupo_preguntas['preguntas']
        justificacion = grupo_preguntas['justificacion']

        enunciados_pregunta = preguntas['enunciados_pregunta']
        opciones_pregunta = preguntas['opciones_pregunta']

        del preguntas['enunciados_pregunta']
        del preguntas['enunciados_pregunta']

        preguntas_data = preguntas

        del grupo_preguntas['enunciados_grupo_pregunta']
        del grupo_preguntas['preguntas']
        del grupo_preguntas['preguntas']
        del grupo_preguntas['justificacion']

        grupo_preguntas_serializer = self.serializer_class(data = grupo_preguntas, context = grupo_preguntas)

        if grupo_preguntas_serializer.is_valid():
            error = grupo_preguntas_serializer.errors
        else:
            validar_errores = True
            error = grupo_preguntas_serializer.errors

        justificacion_serializer = JustificacionSerializer(data = justificacion, context = justificacion)

        if justificacion_serializer.is_valid():
            error = justificacion_serializer.errors
            errores_jsutificacion = {'justificacion': error}
        else:
            validar_errores = True
            error = justificacion_serializer.errores
            errores_justificacion = {'justificacion': error}
        error.update(errores_jsutificacion)

        for indice, enunciado_grupo in enumerate(enunciados_grupo_pregunta):
            enunciados_grupo_pregunta_serializer = EnunciadoGrupoPreguntaSerializer(data = enunciados_grupo_pregunta)
            if enunciados_grupo_pregunta_serializer.is_valid():
                enunciado_grupo = EnunciadoGrupoPregunta(
                    enunciado_general = enunciados_grupo_pregunta_serializer.validated_data['enunciado_general'],
                    grupo_pregunta = enunciados_grupo_pregunta_serializer.validated_data['grupo_pregunta']
                )
                error = enunciados_grupo_pregunta_serializer.errors
            else:
                validar_errores = True
                errores_enunciado_grupo_pregunta = enunciados_grupo_pregunta_serializer.errors

        error.update(errores_enunciado_grupo_pregunta)