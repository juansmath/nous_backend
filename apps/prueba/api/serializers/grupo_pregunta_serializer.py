from rest_framework import serializers

from apps.prueba.api.serializers.pregunta_serializer import PreguntaDetalleSerializer

from apps.prueba.models import GrupoPregunta, EnunciadoGrupoPregunta

class EnunciadoGrupoPreguntaSerializer(serializers.ModelSerializer):
    def validate_enunciado_general(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_grupo_general(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar un grupo de preguntas')
        return value

    class Meta:
        model = EnunciadoGrupoPregunta
        exclude = ('estado',)

class EnunciadoGrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnunciadoGrupoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado_grupo_preguntas':{
                'id': instance.id,
                'enunciado_general': instance.enunciado_general,
                'grupo_pregunta':instance.grupo_pregunta if instance.grupo_pregunta is not None else ''
            }
        }

class GrupoPreguntaSerializer(serializers.ModelSerializer):
    def validate_cantidad_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

class GrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    pregunta = PreguntaDetalleSerializer(many = True, read_only = True)

    class Meta:
        model = GrupoPregunta
        fields = ['id','cantidad_preguntas','preguntas','fecha_creacion']


    def to_representation(self, instance):
        return {
            'grupo_preguntas':{
                'id': instance.id,
                'cantidad_preguntas': instance.cantidad_max_preguntas,
                'preguntas': self.preguntas
            }
        }
