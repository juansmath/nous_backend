from rest_framework import serializers
from apps.prueba.models import Pregunta, EnunciadoPregunta, Justificacion, OpcionPregunta

class JustificacionSerializer(serializers.ModelSerializer):
    def validate_afirmacion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_evidencia(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = Justificacion
        exclude = ('estado',)

class JustificacionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificacion
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'afirmacion': instance.afirmacion,
            'evidencia': instance.evidencia,
            'justificacion': instance.justificacion,
        }

class EnunciadoPreguntaSerializer(serializers.ModelSerializer):
    def valdiate_enunciado(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validation_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar una pregunta')
        return value

    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado',)

class EnunciadoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado', 'fecha_creacion','fecha_actualizacion', 'fecha_eliminacion')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'enunciado': instance.enunciado,
            'pregunta': instance.pregunta.id if instance.pregunta.id is not None else ''
        }

class OpcionPreguntaSerializer(serializers.ModelSerializer):
    def validate_contenido_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Este campo es obligatorio')
        return value

    def validate_letra(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = OpcionPregunta
        exclude = ('estado',)

class OpcionPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'contenido': instance.contenido_opcion,
            'letra': instance.letra,
            'pregunta': instance.pregunta.id if instance.pregunta.id is not None else ''
        }

class PreguntaSerializer(serializers.ModelSerializer):
    competencia_id = serializers.IntegerField(write_only=True)
    justificacion_id = serializers.IntegerField(write_only=True)
    modulo_id = serializers.IntegerField(write_only=True)
    respuesta_id = serializers.IntegerField(write_only=True)
    banco_preguntas_id = serializers.IntegerField(write_only=True)
    nivel_dificultad_id = serializers.IntegerField(write_only=True)
    docente_id = serializers.IntegerField(write_only=True, required=False, default=None)
    # grupo_id = serializers.IntegerField(write_only=True, required=False, default=None)

    def validate_respuesta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar la respuesta')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe crear una justificación')
        return value

    def validate_nivel_dificultad(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar un nivel de dificultad!')
        return value

    class Meta:
        model = Pregunta
        exclude = ('estado',)
        depth = 1

class PreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        opciones = OpcionPregunta.objects.filter(pregunta = instance.id, estado = True)
        opciones_serializer = OpcionPreguntaDetalleSerializer(opciones ,many = True)

        justificacion = Justificacion.objects.filter(id = instance.justificacion.id, estado = True)
        justificacion_serializer = JustificacionDetalleSerializer(justificacion, many = True)

        enunciados = EnunciadoPregunta.objects.filter(pregunta = instance.id, estado = True)
        enunciados_serializer = EnunciadoPreguntaDetalleSerializer(enunciados, many = True)

        return {
            'pregunta':{
                'justificacion': justificacion_serializer.data,
                'enunciados': enunciados_serializer.data,
                'opciones':opciones_serializer.data,
            },
        }

class PreguntaHojaRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        exclude = ('estado',)

        def to_representation(self, instance):
            return {
                'pregunta':{
                    'id': instance.id,
                    'respuesta': instance.respuesta.id if instance.respuesta.id is not None else '',
                }
            }