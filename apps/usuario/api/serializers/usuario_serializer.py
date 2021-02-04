from rest_framework import serializers

from apps.usuario.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

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
