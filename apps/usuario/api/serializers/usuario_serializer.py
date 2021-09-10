from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.persona.api.serializers import PersonaDetalleSerializer
from django.contrib.auth.password_validation import validate_password

from apps.usuario.models import Usuario
from apps.persona.models import Persona

class UsuarioSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Usuario.objects.all())]
        )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        exclude = (
            'last_login',
            'groups',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden!"})

        return attrs

    def create(self, validated_data):
        usuario = Usuario.objects.create(
            email = validated_data['email'],
            username = validated_data['username']
        )

        usuario.set_password(validated_data['password'])
        print(usuario)
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
