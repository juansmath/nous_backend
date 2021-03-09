from rest_framework import serializers
from apps.prueba.models import Pregunta, EnunciadoPregunta, Justificacion, OpcionPregunta
from .general_serializer import OpcionRespuestaSerializer

class EnunciadoPreguntaSerializer(serializers.ModelSerializer):
    def valdiate_enunciado(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validation_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar una pregunta')
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado',)

class EnunciadoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado_pregunta':{
                'id': instance.id,
                'enunciado': instance.enunciado,
                'pregunta': instance.pregunta if instance.pregunta is not None else ''
            }
        }

class JustificacionSerializer(serializers.ModelSerializer):
    def validate_afirmacion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_evidencia(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_solucion(self, value):
        if value == '':
            raise serializers.ValdiationError('Debe seleccionar una opcion de respuesta')

    class Meta:
        model = Justificacion
        exclude = ('estado',)

class JustificacionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificacion
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'justificacion':{
                'id': instance.id,
                'afirmacion': instance.afirmacion,
                'evidencia': instance.evidencia,
                'justificacion': instance.justificacion,
                'solucion': instance.solucion.id if instance.solucion.id is not None else ''
            }
        }

class OpcionPreguntaSerializer(serializers.ModelSerializer):
    def validate_contenido_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Este campo es obligatorio')
        return value

    def validate_letra(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = OpcionPregunta
        exclude = ('estado',)

class OpcionPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado':{
                'id': instance.id,
                'contenido_opcion': instance.contenido_enunciado,
                'letra': instance.letra,
                'pregunta': instance.pregunta if instance.pregunta is not None else ''
            }
        }

class PreguntaSerializer(serializers.ModelSerializer):
    def validate_respuesta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar la respuesta')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe selecionar una justificación')
        return value

    def create(self, validated_data):
        print(validated_data);

    class Meta:
        model = Pregunta
        exclude = ('estado',)

class PreguntaDetalleSerializer(serializers.ModelSerializer):
    opcion = OpcionPreguntaDetalleSerializer(many = True, read_only = True)
    respuesta = OpcionRespuestaSerializer(many = True, read_only = True)
    justificacion = JustificacionDetalleSerializer(many = True, read_only = True)

    class Meta:
        model = Pregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'pregunta':{
                'id': instance.id,
                'enunciados': instance.enunciado,
                'grupo': instance.grupo.id if instance.grupo.id is not None else '',
                'opciones': self.opcion,
                'respuesta': self.respuesta,
                'justificacion': self.justificacion
            }
        }