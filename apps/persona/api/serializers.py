from rest_framework import serializers

from apps.persona.models import Persona
from apps.usuario.models import Usuario

class PersonaSerializer(serializers.ModelSerializer):
    def validate_identificacion(self, value):
        if value is None or value == '':
            raise serializers.ValidationError('Identificación es obligatorio')
        return value

    def validate_primer_nombre(self, value):
        if value == '':
            raise serializers.ValidationError('Primer nombre es obligatorio')
        return value

    def validate_primer_apellido(self, value):
        if value == '':
            raise serializers.ValidationError('Primer apellido es obligatorio')
        return value

    def validate_telefono(self, value):
        if value == '':
            raise serializers.ValidationError('Número de telefono es obligatorio')
        return value

    def validate_fecha_nacimiento(self, value):
        if value == '':
            raise serializers.ValidationError('Campo es obligatorio')
        return value

    class Meta:
        model = Persona
        exclude = ('estado',)

class PersonaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'identificacion': instance.identificacion,
            'primer_nombre': instance.primer_nombre,
            'segundo_nombre': instance.segundo_nombre if instance.segundo_nombre is not None else '',
            'primer_apellido': instance.primer_apellido,
            'segundo_apellido': instance.segundo_apellido if instance.segundo_apellido is not None else '',
            'genero': instance.genero,
            'rh': instance.rh,
            'estado_civil': instance.estado_civil,
            'telefono': instance.telefono,
            'fecha_nacimiento': instance.fecha_nacimiento,
            'usuario_id': instance.usuario_id
        }
