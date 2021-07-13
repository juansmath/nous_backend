from rest_framework import serializers
from apps.prueba.api.serializers.pregunta_serializer import PreguntaDetalleSerializer
from apps.prueba.api.serializers.general_serializer import CompetenciaSerializer
from apps.prueba.api.serializers.grupo_pregunta_serializer import GrupoPreguntaDetalleSerializer

from apps.prueba.models import BancoPreguntas, Pregunta,GrupoPregunta, Competencia

class BancoPreguntasSerializer(serializers.ModelSerializer):
    def validate_nombre_banco(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_modulo(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar un módulo')
        return value

    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

class BancoPreguntasDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

    def to_representation(self, instance):
        competencia = Competencia.objects.filter(id = instance.competencia.id, estado = True)
        competencias_serializer = CompetenciaSerializer(competencia, many = True)

        preguntas = Pregunta.objects.filter(banco_preguntas = instance.id, estado = True, grupo__exact = "")
        preguntas_serializer = PreguntaDetalleSerializer(preguntas, many = True)

        grupos_preguntas = GrupoPregunta.objects.filter(banco_preguntas = instance.id, estado = True)
        grupos_preguntas_serializer = GrupoPreguntaDetalleSerializer(grupos_preguntas, many = True)

        return {
            'info':{
                'id': instance.id,
                'nombre': instance.nombre_banco,
                'modulo': instance.modulo.id if instance.modulo.id is not None else ''
            },
            'competencias': competencias_serializer.data,
            'preguntas': preguntas_serializer.data,
            'grupos_preguntas': grupos_preguntas_serializer.data
        }