from rest_framework import serializers

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasDetalleSerializer
from apps.prueba.api.serializers.general_serializer import OpcionRespuestaSerializer, ModuloSerializer, NivelEjecucionSerializer
from apps.docente.api.serializers import DocenteSerializer
from apps.estudiante.api.serializers import EstudianteSerializer

from apps.prueba.models import (Prueba, ResultadoPrueba, HojaRespuesta, BancoPreguntas,
                                OpcionRespuesta, Modulo, NivelEjecucion, PruebasEstudiante)
from apps.estudiante.models import Estudiante
from apps.docente.models import Docente

class PruebaSerializer(serializers.ModelSerializer):
    def validate_nombre_prueba(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_limite_tiempo(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_numero_intentos(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = Prueba
        exclude = ('estado',)

class PruebaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        exclude = ('estado')

    def to_representation(self, instance):
        banco_preguntas = BancoPreguntas.objects.filter(id = instance.banco_preguntas, estado = True)
        banco_preguntas_serializer = BancoPreguntasDetalleSerializer(banco_preguntas, many = True)

        docente = Docente.objects.filter(id = instance.docente, estado = True).first()
        docente_serializer = DocenteSerializer(docente)

        return {
            'pregunta':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            },
            'banco_preguntas': banco_preguntas_serializer.data,
            'docente': docente_serializer.data
        }

class PruebaEstudianteSerializer(serializers.ModelSerializer):
    def validate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_prueba(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = PruebasEstudiante
        exclude = ('estado',)

class PruebaEstudianteDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PruebasEstudiante
        exclude = ('estado',)

    def to_representation(self, instance):
        prueba = Prueba.objects.filter(id = instance.prueba, estado = True).first()
        prueba_serializer = PruebaSerializer(prueba, many = True)

        estudiante = Estudiante.objects.filter(id = instance.estudiante).select_related('persona')
        return {
            'id': instance.id,
            'prueba': prueba_serializer.data,
            'estudiante': instance.estudiante.id,
            'presentada': instance.presentada
        }

class HojaRespuestaSerializer(serializers.ModelSerializer):
    def validate_prueba_asignada(self, value):
        if value == '':
            raise serializers.ValidationError('Debe haberse seleccionado una prueba')
        return value

    def validate_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar una pregunta')
        return value

    def validate_opcion_marcada(self, value):
        if value == '':
            raise serializers.ValidationError('Debe maracar una respuesta')
        return value

    def validate_tiempo_empleado_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe agregarse el tiempo para la pregunta')
        return value

    def validate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('Estudiante no seleccionado')
        return value

    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

class HojaRespuestaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

    def to_representation(self, instance):
        opcion_marcada = OpcionRespuesta.objects.filter(id = instance.opcion_marcada)
        opcion_marcada_serializer = OpcionRespuestaSerializer(opcion_marcada, many = True)

        return {
            'hoja_respuesta':{
                'id': instance.id,
                'prueba_asignada': instance.prueba_asignada.id if instance.prueba_asignada.id is not None else '',
                'pregunta': instance.pregunta.id if instance.pregunta.id is not None else '',
                'opcion_marcada': opcion_marcada_serializer.data,
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'tiempo_empleado_pregunta': instance.tiempo_empleado_pregunta,
                'calificacion': instance.calificacion
            }
        }

class ResultadoPruebaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoPrueba
        exclude = ('estado',)

    def to_representation(self, instance):
        hoja_respuestas = HojaRespuesta.objects.filter(prueba__exact = instance.prueba, estudiante__exact = instance.estudiante)
        hoja_respuestas_serializer = HojaRespuestaDetalleSerializer(hoja_respuestas, many = True)

        prueba_asignada = PruebasEstudiante.objects.filter(id = instance.prueba_asignada, estado = True)
        prueba_asignada_serializer = PruebaEstudianteDetalleSerializer(prueba_asignada, many = True)

        modulo = Modulo.objects.filter(id = instance.modulo, estado = True)
        modulo_serializer = ModuloSerializer(modulo, many = True)

        calificacion_final = NivelEjecucion.objects.filter(id = instance.calificacion_final, estado = True)
        calificacion_final_serializer = NivelEjecucionSerializer(calificacion_final, many = True)

        estudiante = Estudiante.objects.filter(id = instance.estudiante, estado = True).first()
        estudainte_serializer = EstudianteSerializer(estudiante, many = True)

        return {
            'resultado_prueba':{
                'id': instance.id,
                'calificacion':instance.calificacion,
                'estudiante': estudainte_serializer.data,
                'docente': instance.docente.id if instance.docente.id is not None else '',
                'modulo': instance.modulo.id if instance.modulo.id is not None else '',
                'prueba_asignada': prueba_asignada_serializer.data,
                'calificada': instance.calificada,
                'numero_aciertos': instance.numero_aciertos,
                'numero_desaciertos': instance.numero_desaciertos,
                'tiempo_empleado': instance.tiempo_empleado,
                'hoja_respuestas': hoja_respuestas_serializer.data,
                'calificacion_final': calificacion_final_serializer.data,
            }
        }

