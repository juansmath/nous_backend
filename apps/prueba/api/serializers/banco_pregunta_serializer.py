from rest_framework import serializers
from apps.prueba.api.serializers.pregunta_serializer import PreguntaDetalleSerializer
from apps.prueba.api.serializers.general_serializer import CompetenciaSerializer
from apps.prueba.api.serializers.grupo_pregunta_serializer import GrupoPreguntaDetalleSerializer

from apps.prueba.models import BancoPreguntas, Pregunta,GrupoPregunta, Competencia

class BancoPreguntasSerializer(serializers.ModelSerializer):
    # pregunta = serializers.PrimaryKeyRelatedField(allow_empty = True, many = True, queryset=Pregunta.objects.all())
    # grupo_pregunta = serializers.PrimaryKeyRelatedField(allow_empty = True, many = True, queryset=GrupoPregunta.objects.all())

    def validate_nombre_banco(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

class BancoPreguntasDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

    def to_representation(self, instance):
        competencias = Competencia.objects.filter(id_referencia = instance.id, estado = True)
        competencias_serializer = CompetenciaSerializer(competencias, many = True)

        preguntas = Pregunta.objects.filter(id_referencia = instance.id, estado = True)
        preguntas_serializer = PreguntaDetalleSerializer(preguntas, many = True)

        grupos_preguntas = GrupoPregunta.objects.filter(id_referencia = instance.id, estado = True)
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