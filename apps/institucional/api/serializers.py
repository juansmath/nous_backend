from rest_framework import serializers

from apps.institucional.models import Facultad, Programa, NivelAcademico

class FacultadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facultad
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'codigo_facultad': instance.codigo_facultad,
            'nombre_facultad': instance.nombre_facultad
        }

class ProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programa
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'data':{
                'id': instance.id,
                'codigo_programa': instance.codigo_programa,
                'nombre_programa': instance.nombre_programa,
                'creditos': instance.creditos,
                'semestres': instance.semestres,
                'facultad': instance.facultad.id if instance.facultad.id is not None else ''
            },
        }