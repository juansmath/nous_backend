from rest_framework import serializers

from apps.persona.api.serializers import PersonaDetalleSerializer

from apps.usuario.models import Usuario
from apps.persona.models import Persona

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        exclude = (
            'last_login',
            'groups',
            'password',
        )

    def crear_usuario(self, validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

    def actualizar_usuario(self, instance, validated_data):
        actualizar_usuario = super().update(instance, validated_data)
        actualizar_usuario.set_password(validated_data['password'])
        actualizar_usuario.save()
        return actualizar_usuario

    def to_representation(self, instance):
        datos_usuario = Persona.objects.filter(usuario_id = instance.id).first()
        datos_usuario_serializer = PersonaDetalleSerializer(datos_usuario)
        return {
            'id': instance.id,
            'username': instance.username,
            'email': instance.email,
            'persona': datos_usuario_serializer.data
        }
