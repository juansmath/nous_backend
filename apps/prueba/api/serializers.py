from rest_framework import serializers

from apps.prueba.models import Modulo, Competencia, GrupoPregunta, OpcionRespuesta, OpcionEnunciado, Justificacion, Pregunta, BancoPregunta

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        exclude = ('estado',)

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        exclude = ('estado',)

class GrupoPreguntaSerializer(serializers.ModelSerializer):
    cantidad_max_preguntas = serializers.IntegerField(max_length = 10)

    def validate_unuciado_general(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_cantidad_max_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

class GrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'grupo_preguntas':{
                'id': instance.id,
                'ununciado_general': instance.enunciado_general,
                'cantidad_max_preguntas': instance.cantidad_max_preguntas
            }
        }

class OpcionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionRespuesta
        exclude = ('estado',)

class OpcionEnunciadoSerializer(serializers.ModelSerializer):
    LETRAS_OPCION = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),
        ('G','G'),
        ('H','H'),
        ('I','I')
    ]
    contenido_opcion = serializers.CharField(max_length = 250)
    letra = serializers.ChoiseField(choices = LETRAS_OPCION)

    def validate_contenido_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('El campos es obligatorio')
        return value

    def validate_letra(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = OpcionEnunciado
        exclude = ('estado',)

class OpcionEnunciadoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionEnunciado
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado':{
                'id': instance.id,
                'contenido_opcion': instance.contenido_enunciado,
                'letra': instance.letra
            }
        }

class JustificacionSerializer(serializers.ModelSerializer):
    afirmacion = serializers.CharField(max_length = 250)
    evidencia = serializers.CharField(max_length = 250)

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

class PreguntaSerializer(serializers.ModelSerializer):
    def valdiate_enunciado(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def valdiate_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe existir uno(s) para la pregunta')
        return value

    def validate_respuesta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar la respuesta')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe selecionar una justificación')
        return value

    class Meta:
        model = Pregunta
        exclude = ('estado',)

class PreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'pregunta':{
                'id': instance.id,
                'enunciado': instance.enunciado,
                'grupo': instance.grupo.id if instance.grupo.id is not None else '',
                'opcion': instance.opcion.id if instance.opcion.id is not None else '',
                'respuesta': instance.respuesta.id if instance.respuesta.id is not None else '',
                'justificacion': instance.justificacion.id if instance.justificacion.id is not None else ''
            }
        }
