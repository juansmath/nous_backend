from rest_framework import serializers

from apps.prueba.models import Modulo, Competencia, OpcionRespuesta

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        exclude = ('estado',)

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        exclude = ('estado',)

class OpcionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionRespuesta
        exclude = ('estado','fecha_creacion', 'fecha_eliminacion', 'fecha_actualizacion')