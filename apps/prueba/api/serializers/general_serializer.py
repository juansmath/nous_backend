from rest_framework import serializers

from apps.prueba.models import Modulo, Competencia, NivelEjecucion, DescripcionNivelEjecucion

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        exclude = ('estado',)

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        exclude = ('estado',)

class DescripcionesNivelesEjecucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionNivelEjecucion
        exclude = ('estado','fecha_creacion', 'fecha_eliminacion', 'fecha_actualizacion')

class DescripcionNivelEjecucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DescripcionNivelEjecucion
        exclude = ('estado','fecha_creacion', 'fecha_eliminacion', 'fecha_actualizacion')

    def to_representation(self, instance):
        descripciones_especificas = DescripcionNivelEjecucion.objects.filter(nivel_ejecucion_id = instance.id)
        descripciones_especificas_serializer = DescripcionNivelEjecucionSerializer(descripciones_especificas, many = True)

        return {
            'id': instance.id,
            'nivel': instance.nivel,
            'puntaje_minimo': instance.puntaje_minimo,
            'puntaje_maximo': instance.puntaje_maximo,
            'descripcion_general': instance.descripcion_general,
            'modulo': instance.modulo.id if instance.modulo.id is not None else '',
            'descripciones_especificas': descripciones_especificas_serializer.data
        }

class NivelEjecucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelEjecucion
        exclude = ('estado','fecha_creacion', 'fecha_eliminacion', 'fecha_actualizacion')