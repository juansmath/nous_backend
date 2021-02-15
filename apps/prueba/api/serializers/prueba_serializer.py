from rest_framework import serializers

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasDetalleSerializer

from apps.prueba.models import Prueba, ResultadoPrueba, HojaRespuesta, BancoPreguntas
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
        banco_preguntas = BancoPreguntas.objects.filter(id_referencia = isinstance.id, estado = True)
        banco_preguntas_serializer = BancoPreguntasDetalleSerializer(banco_preguntas, many = True)

        return {
            'info':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            },
            'banco_preguntas': banco_preguntas_serializer.data
        }

class HojaRespuestaSerializer(serializers.ModelSerializer):
    def validate_prueba(self, value):
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
        return {
            'hoja_respuesta':{
                'id': instance.id,
                'prueba': instance.prueba.id if instance.prueba.id is not None else '',
                'grupo_preguntas': instance.grupo_preguntas.id if instance.grupo_preguntas.id is not None else '',
                'pregunta': instance.pregunta.id if instance.pregunta.id is not None else '',
                'opcion_marcada': instance.opcion_marcada.id if instance.opcion_marcada.id is not None else '',
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'tiempo_empleado': instance.tiempo_empleado
            }
        }

class ResultadoPruebaSerializer(serializers.ModelSerializer):
    def valdiate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionarse un estudiante')
        return value

        def validate_docente(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar el docente a cargo')
            return value

        def validate_modulo(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar un módulo')
            return value

        def validate_prueba(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar un módulo')
            return value

        def valdiate_hoja_respuesta(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar la hoja de respuestas')
            return value

        class Meta:
            model = ResultadoPrueba
            exclude = ('estado',)

class ResultaddoPruebaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoPrueba
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'resultado_prueba':{
                'id': instance.id,
                'calificacion':instance.calificacion,
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'docente': instance.docente.id if instance.docente.id is not None else '',
                'modulo': instance.modulo.id if instance.modulo.id is not None else '',
                'prueba': instance.prueba.id if instance.prueba.id is not None else '',
                'hoja_respuesta': instance.hoja_respuesta.id if instance.hoja_respuesta.id is not None else ''
            }
        }
