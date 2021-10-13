import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action

from datetime import time, datetime, timedelta

from apps.prueba.api.serializers.prueba_serializer import *

from apps.prueba.models import Prueba, PruebasEstudiante, HojaRespuesta

class PruebaViewSet(viewsets.ViewSet):
    model = Prueba
    serializer_class = PruebaSerializer

    def list(self, request):
        pruebas = self.model.objects.filter(estado = True)
        prueba_serializer = PruebaSerializer(pruebas, many = True)
        return Response(prueba_serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        prueba_serializer = self.serializer_class(data = request.data)
        if prueba_serializer.is_valid():
            prueba_serializer.save()
            return Response({'mensaje':'Se registro correctamente la prueba'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos!', 'error': prueba_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        prueba = self.model.objects.get(id = kwargs['pk'], estado=True)
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba_serializer = self.serializer_class(prueba, request.data)
        if prueba_serializer.is_valid():
            prueba_serializer.update(prueba, request.data)
            return Response({'mensaje':'Se actualizo correctamente la prueba!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos', 'error': prueba_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        prueba = self.model.objects.filter(id = kwargs['pk']).first()
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba_serializer = PruebaSerializer(prueba)
        return Response(prueba_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        prueba = self.model.objects.filter(id = kwargs['pk']).first()
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba.delete()
        return Response({'mensaje':'La prueba se borro exitosamente!'}, status=status.HTTP_200_OK)

class PruebasEstudianteAsignarViewSet(viewsets.ViewSet):
    model = PruebasEstudiante
    serializer_class = PruebaEstudianteSerializer

    def crear_asignacion_prueba_estudiantes(self, estudiantes=[]):
        validar_errores = False
        asignaciones_prueba_validas, errores_asignacion_prueba = [], []

        for indice, estudiante in enumerate(estudiantes):
            asignacion_prueba_serializer = PruebaEstudianteSerializer(data=estudiante)
            if asignacion_prueba_serializer.is_valid():
                asignacion = PruebasEstudiante(
                    estudiante = asignacion_prueba_serializer.validated_data['estudiante'],
                    prueba = asignacion_prueba_serializer.validated_data['prueba']
                )
                asignaciones_prueba_validas.append(asignacion)
            else:
                validar_errores = True
                errores_asignacion_prueba.append(asignacion_prueba_serializer.errors)

        return {
            'validar_errores': validar_errores,
            'asignaciones_prueba_validas': asignaciones_prueba_validas,
            'errores_asignacion_prueba': errores_asignacion_prueba
        }

    def create(self, request):
        validar_errores = False
        asignaciones_prueba_validas = []
        errores_asignacion_prueba, error = [], {}

        datos_asignaciones = self.crear_asignacion_prueba_estudiantes(request.data['estudiantes'])

        validar_errores = datos_asignaciones['validar_errores']
        asignaciones_prueba_validas = datos_asignaciones['asignaciones_prueba_validas']
        errores_asignacion_prueba = {'errores_asignacion': datos_asignaciones['errores_asignacion_prueba']}
        error.update(errores_asignacion_prueba)

        if validar_errores:
            return Response({'error':'Ocurrió un error al asignar la prueba a los estudiantes!', 'error':error}, status=status.HTTP_400_BAD_REQUEST)

        for estudiante in asignaciones_prueba_validas:
            estudiante.save()

        return Response({'mensaje': 'Se asigno correctamente la prueba a los estudiantes'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        validar_errores = False
        asignaciones_prueba_validas = []
        errores_asignacion_prueba, error = [], {}

        borrar_asignaciones = request.data['borrar_asignaciones']

        datos_asignacion_prueba = self.model.objects.filter(id= kwargs['pk']).first()

        if not datos_asignacion_prueba:
            return Response({'mensaje':'No existe una asiganción prueba con estos datos!'}, status = status.HTTP_400_BAD_REQUEST)

        datos_asignaciones = self.crear_asignacion_prueba_estudiantes(request.data['estudiantes'])

        validar_errores = datos_asignaciones['validar_errores']
        asignaciones_prueba_validas = datos_asignaciones['asignaciones_prueba_validas']
        errores_asignacion_prueba = {'errores_asignacion': datos_asignaciones['errores_asignacion_prueba']}

        error.update(errores_asignacion_prueba)

        if validar_errores:
            return Response({'mensaje':'Ocurrió un error al asignar la prueba a los estudaintes!'}, error, status=status.HTTP_400_BAD)

        for asignacion in borrar_asignaciones:
            self.model.objects.filter(id = kwargs['pk']).delete()

        for estudiante in asignaciones_prueba_validas:
            estudiante.save()

        return Response({'mensaje': 'Se actualizo correctamente la asignación de la prueba!'}, status=status.HTTP_201_CREATED)

    # @action(methods=['get'], detail=False, url_path='')
    # def obtener_estudiantes_prueba_asignada(self, request):
    #     datos_asignacion_prueba = self.model.objects.filter(prueba = request.prueba, estado = True)

    #     if not datos_asignacion_prueba:
    #         return Response({'error':'No existe una prueba asignada con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

    #     datos_asignacion_prueba_serializer = PruebaEstudianteDetalleSerializer(datos_asignacion_prueba, many = True)
    #     return Response(datos_asignacion_prueba_serializer.data, status=status.HTTP_200_OK)

class ResultadosPruebaViewSet(viewsets.ViewSet):
    model = PruebasEstudiante
    serializer_class = PruebaEstudianteDetalleSerializer

    def list(self, request):
        resultados_pruebas = self.model.objects.filter(estado=True)
        resultados_prueba_serializer = PruebaEstudianteDetalleSerializer(resultados_pruebas, many=True)
        return Response(resultados_prueba_serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='')
    def obtener_resultados_prueba_estudiante(self, request):
        datos = json.loads(request.query_params.get('datos'))
        resultados_prueba = self.model.objects.get(estudiante=datos['estudiante'], prueba=datos['prueba'], presentada=True)

        if not resultados_prueba:
            return Response({'mensaje':'El resultado de la prueba a la que esta accediendo no se ha presentado u asignado'}, status=status.HTTP_400_BAD_REQUEST)
        print(resultados_prueba)
        resultados_prueba_serializer = PruebaEstudianteSerializer(resultados_prueba)
        return Response(resultados_prueba_serializer.data, status=status.HTTP_200_OK)
        # return Response(status=status.HTTP_200_OK)

class PresentarPruebaEstudianteViewSet(viewsets.ViewSet):
    model = HojaRespuesta
    serializer_class = HojaRespuestaSerializer

    def create(self, request):
        validar_errores = False
        respuestas_validas, hoja_respuestas_error,error = [], [],{}
        calificacion_final, tiempo_empleado, numero_aciertos, numero_desaciertos = 0, 0, 0, 0

        datos = request.data['hoja_respuesta']

        prueba_estudiante = PruebasEstudiante.objects.filter(id=request.data['prueba_asignada'],
                                                             estudiante=request.data['estudiante']).first()

        if not prueba_estudiante:
            return Response({ 'mensaje': 'La prueba seleccionada no ha sido asignada al estudiante!'},
                            status = status.HTTP_400_BAD_REQUEST)

        if prueba_estudiante.presentada:
            return Response({ 'mensaje': 'La prueba ya ha sido presentada por el estudiante!'},
                            status = status.HTTP_400_BAD_REQUEST)

        for indice, hoja_respuesta in enumerate(datos):
            hoja_respuesta_serializer = self.serializer_class(data = hoja_respuesta)
            if hoja_respuesta_serializer.is_valid():
                respuesta_valida = HojaRespuesta(
                    prueba_asignada = hoja_respuesta_serializer.validated_data['prueba_asignada'],
                    pregunta = hoja_respuesta_serializer.validated_data['pregunta'],
                    opcion_marcada = hoja_respuesta_serializer.validated_data['opcion_marcada'],
                    estudiante = hoja_respuesta_serializer.validated_data['estudiante'],
                    tiempo_empleado_pregunta = hoja_respuesta_serializer.validated_data['tiempo_empleado_pregunta'],
                    calificacion = hoja_respuesta_serializer.validated_data['calificacion'],
                )
                respuestas_validas.append(respuesta_valida)

                tiempo_pregunta = time.fromisoformat(str(hoja_respuesta_serializer.validated_data['tiempo_empleado_pregunta']))

                segundos_pregunta = timedelta(hours=tiempo_pregunta.hour, minutes=tiempo_pregunta.minute, seconds=tiempo_pregunta.second)

                tiempo_empleado += segundos_pregunta.total_seconds()

                if hoja_respuesta['calificacion'] == True:
                     numero_aciertos += 1
                     calificacion_final += hoja_respuesta['valor_pregunta']
                else:
                    numero_desaciertos += 1

            else:
                validar_errores = True
                hoja_respuestas_error.append({
                    'indice': indice,
                    'hoja_respuesta': hoja_respuesta_serializer.errors
                })

        hoja_respuestas_error = {'hoja_respuestas_error': hoja_respuestas_error}
        error.update(hoja_respuestas_error)

        if validar_errores:
            return Response({'mensaje': 'Existen errores en la hoja de respuestas!', 'error': error}, status = status.HTTP_400_BAD_REQUEST)

        if len(respuestas_validas) != 0:
            datos_nivel_ejecucion = NivelEjecucion.objects.filter(modulo = prueba_estudiante.modulo)
            for nivel_ejecucion in datos_nivel_ejecucion:
                if calificacion_final <= nivel_ejecucion.puntaje_maximo:
                    prueba_estudiante.nivel_ejecucion = nivel_ejecucion

            tiempo_empleado = timedelta(seconds=tiempo_empleado)

            prueba_estudiante.calificada = True
            prueba_estudiante.presentada = True
            prueba_estudiante.numero_desaciertos = numero_desaciertos
            prueba_estudiante.numero_aciertos = numero_aciertos
            prueba_estudiante.puntaje_prueba = calificacion_final
            prueba_estudiante.tiempo_empleado = timedelta.__str__(tiempo_empleado)

            prueba_estudiante.save()

            for hoja in respuestas_validas:
                hoja.resultado_prueba = prueba_estudiante

            self.model.objects.bulk_create(respuestas_validas)

        return Response({'mensaje':'Se registro correctamente las respuestas'}, status=status.HTTP_200_OK)