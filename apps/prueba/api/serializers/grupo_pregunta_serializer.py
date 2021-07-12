from rest_framework import serializers

from apps.prueba.api.serializers.pregunta_serializer import PreguntaDetalleSerializer

from apps.prueba.models import GrupoPregunta, EnunciadoGrupoPregunta, Pregunta

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
                'enunciado_general': instance.enunciado_general
            }
        }

class GrupoPreguntaSerializer(serializers.ModelSerializer):
    def validate_cantidad_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_banco_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('Debe asociarse un banco al grupo de preguntas')
        return value

    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

class GrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoPregunta
        fields = ['id','cantidad_preguntas','nombre_grupo','fecha_creacion']

    def to_representation(self, instance):
        enunciados_grupo = EnunciadoGrupoPregunta.objects.filter(grupo_id = instance.id, estado = True)
        enunciado_grupo_serializer = EnunciadoGrupoPreguntaDetalleSerializer(enunciados_grupo, many = True)

        preguntas = Pregunta.objects.filter(grupo_id = instance.id, estado = True)
        preguntas_serializer = PreguntaDetalleSerializer(preguntas, many = True)

        return {
            'grupo_preguntas':{
                'id': instance.id,
                'nombre_grupo': instance.nombre_grupo,
                'enunciados_grupo_preguntas': enunciado_grupo_serializer.data,
                'cantidad_preguntas': instance.cantidad_preguntas,
                'preguntas': preguntas_serializer.data
            }
        }
