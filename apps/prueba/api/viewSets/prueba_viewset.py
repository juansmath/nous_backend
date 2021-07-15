import json

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from apps.prueba.api.serializers.prueba_serializer import *

from apps.prueba.models import Prueba, PruebasEstudiante, HojaRespuesta, ResultadoPrueba

class PruebaViewSet(viewsets.ViewSet):
    model = Prueba
    serializer_class = PruebaSerializer

    def list(self, request):
        pruebas = self.model.objects.filter(estado = True)
        prueba_serializer = PruebaSerializer(pruebas, many = True)
        return Response(prueba_serializer.data, status = status.HTTP_200_OK)

    def create(self, request):
        prueba_serializer = self.serializer_class(request.data)
        if prueba_serializer.is_valid():
            prueba_serializer.save()
            return Response({'mensaje':'Se registro correctamente la prueba'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos!', 'error': prueba_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        prueba = self.model.objects.filter(id = kwargs['pk']).first()
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba_serializer = self.serializer_class(prueba, request.data)
        if prueba_serializer.is_valid():
            prueba_serializer.update(prueba, request.data)
            return Response({'mensaje':'Se actualizo correctamente la pregunta!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'mensaje':'Existen errores en los campos', 'error': prueba_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        prueba = self.model.objects.filter(id = kwargs['pk']).first()
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba_serializer = PruebaDetalleSerializer(prueba, many = True)
        return Response(prueba_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        prueba = self.model.objects.filter(id = kwargs['pk']).first()
        if not prueba:
            return Response({'mensaje':'No existe una prueba con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        prueba.delete()
        return Response({'mensaje':'La prueba se borro exitosamente!'}, status=status.HTTP_200_OK)

class PruebasEstudianteViewSet(viewsets.ViewSet):
    model = PruebasEstudiante
    serializer_class = PruebaEstudianteSerializer

    def crear_asignacion_prueba_estudaintes(self, asignaciones=[]):
        validar_errores = False
        asignaciones_prueba_validas, errores_asignacion_prueba = [], []

        for indice, estudiante in enumerate(asignaciones):
            asignacion_prueba_serializer = PruebaEstudianteSerializer(estudiante)
            if asignacion_prueba_serializer.is_valid():
                asignacion = PruebasEstudiante(
                    estudiante = asignacion_prueba_serializer.validated_data['estudiante'],
                    prueba = asignacion_prueba_serializer.validated_data['prueba']
                )
                asignaciones_prueba_validas.append(asignacion)
            else:
                validar_errores = True
                errores_asignacion_prueba[indice] = asignacion_prueba_serializer.errors

        return {
            'validar_errores': validar_errores,
            'asignaciones_prueba_validas': asignaciones_prueba_validas,
            'errores_asignacion_prueba': errores_asignacion_prueba
        }

    def create(self, request):
        validar_errores = False
        asignaciones_prueba_validas = []
        errores_asignacion_prueba, error = [], {}

        asignacion_prueba_estudiantes = request['asignacion_prueba_estudiantes']

        datos_asignaciones = self.crear_asignacion_prueba_estudaintes(asignacion_prueba_estudiantes)

        validar_errores = datos_asignaciones['validar_errores']
        asignaciones_prueba_validas = datos_asignaciones['asignaciones_prueba_validas']
        errores_asignacion_prueba = datos_asignaciones['errores_asignacion_prueba']

        error.update(errores_asignacion_prueba)

        if validar_errores:
            return Response({'mensaje':'Ocurrió un error al asignar la prueba a los estudaintes!'}, error, status=status.HTTP_400_BAD)

        self.model.objects.bulk_created(asignaciones_prueba_validas)

        return Response({'mensaje': 'Se asigno correctamente la prueba a los estudiantes'}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        validar_errores = False
        asignaciones_prueba_validas = []
        errores_asignacion_prueba, error = [], {}

        asignacion_prueba_estudiantes = request['asignacion_prueba_estudaintes']
        borrar_asignacion_prueba_estudiantes = request['borrar_asignacion_prueba_estudaintes']

        datos_asignaciones = self.crear_asignacion_prueba_estudaintes(asignacion_prueba_estudiantes)
        if not datos_asignaciones:
            return Response({'error':'No existe una prueba asignada con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        validar_errores = datos_asignaciones['validar_errores']
        asignaciones_prueba_validas = datos_asignaciones['asignaciones_prueba_validas']
        errores_asignacion_prueba = datos_asignaciones['errores_asignacion_prueba']

        error.update(errores_asignacion_prueba)

        if validar_errores:
            return Response({'mensaje':'Ocurrió un error al asignar la prueba a los estudaintes!'}, error, status=status.HTTP_400_BAD)

        for asignacion in borrar_asignacion_prueba_estudiantes:
            self.model.objects.filter(id = kwargs['pk']).delete()

        self.model.objects.bulk_created(asignaciones_prueba_validas)

        return Response({'mensaje': 'Se actualizo correctamente la asignación a los estudiantes'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        datos_asignacion_prueba = self.model.objects.filter(id = kwargs['pk'], estado = True)
        if not datos_asignacion_prueba:
            return Response({'error':'No existe una prueba asignada con los datos suministrados!'}, status=status.HTTP_400_BAD_REQUEST)

        datos_asignacion_prueba_serializer = PruebaEstudianteDetalleSerializer(datos_asignacion_prueba, many = True)
        return Response(datos_asignacion_prueba_serializer.data, status=status.HTTP_200_OK)

class ResultadosPruebaViewSet(viewsets.ViewSet):
    model = ResultadoPrueba
    serializer_class = ResultadoPruebaSerializer

    def list(self, request):
        resultados_pruebas = self.model.objects.filter(estado = True)
        resultados_pruebas_serializer = self.serializer_class(resultados_pruebas, many = True)
        return Response(resultados_pruebas_serializer.data, status=status.HTTP_200_OK)