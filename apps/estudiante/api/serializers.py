from rest_framework import serializers
from apps.prueba.api.serializers import PruebaDetalleSerializer, GrupoPreguntaDetalleSerializer, OpcionRespuestaSerializer, PreguntaDetalleSerializer

from apps.estudiante.models import Estudiante, HojaRespuesta
from apps.prueba.models import Prueba, OpcionRespuesta, GrupoPregunta, Pregunta

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'

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
                'prueba': instance.prueba.id if instance.prueba.id is not None else '',
                'grupo_preguntas': instance.grupo_preguntas.id if instance.grupo_preguntas.id is not None else '',
                'pregunta': instance.pregunta.id if instance.pregunta.id is not None else '',
                'opcion_marcada': instance.opcion_marcada.id if instance.opcion_marcada.id is not None else '',
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'tiempo_empleado': instance.tiempo_empleado
            }
        }