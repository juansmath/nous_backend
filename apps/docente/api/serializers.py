from rest_framework import serializers
from apps.docente.models import Docente
from apps.persona.models import Persona
from apps.institucional.models import NivelAcademico

from apps.institucional.api.serializers import ProgramaSerializer
from apps.persona.api.serializers import PersonaDetalleSerializer
from apps.institucional.api.serializers import NivelAcademicoSerializer

class DocenteSerializer(serializers.ModelSerializer):
    def validate_nivel_academico(self, value):
        if value == '':
            raise serializers.ValidationError('Este campo es obligatorio!')
        return value

    def validate_persona(self, value):
        if value == '':
            raise serializers.ValidationError('Este campo es obligatorio!')
        return value

    class Meta:
        model = Docente
        fields = '__all__'

    def to_representation(self, instance):
        programas = Docente.objects.prefetch_related('programas').get(id = instance.id)
        programas_serializer = ProgramaSerializer(programas, many=True)

        persona = Persona.objects.get(id = instance.persona)
        persona_serializer = PersonaDetalleSerializer(persona)

        nivel_academico = NivelAcademico.objects.get(id = instance.nivel_academico)
        nivel_academico_serializer = NivelAcademicoSerializer(nivel_academico)

        return {
            'id': instance.id,
            'programas': programas_serializer.data,
            'persona': persona_serializer.data,
            'nivel_academico': nivel_academico_serializer.data
        }
