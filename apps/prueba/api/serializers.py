from rest_framework import serializers

from apps.prueba.models import Modulo, Competencia, GrupoPregunta, OpcionRespuesta, OpcionEnunciado, Justificacion, Pregunta, BancoPregunta, Prueba, ResultadoPrueba
from apps.estudiante.models import Estudiante, HojaRespuesta
from apps.docente.models import Docente

from apps.estudiante.api.serializers import Estudiante, HojaRespuesta

class ModuloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modulo
        exclude = ('estado',)

class CompetenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencia
        exclude = ('estado',)

class GrupoPreguntaSerializer(serializers.ModelSerializer):
    cantidad_max_preguntas = serializers.IntegerField(max_length = 10)

    def validate_unuciado_general(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_cantidad_max_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

class GrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'grupo_preguntas':{
                'id': instance.id,
                'ununciado_general': instance.enunciado_general,
                'cantidad_max_preguntas': instance.cantidad_max_preguntas
            }
        }

class OpcionRespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionRespuesta
        exclude = ('estado',)

class OpcionEnunciadoSerializer(serializers.ModelSerializer):
    LETRAS_OPCION = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),
        ('G','G'),
        ('H','H'),
        ('I','I')
    ]
    contenido_opcion = serializers.CharField(max_length = 250)
    letra = serializers.ChoiseField(choices = LETRAS_OPCION)

    def validate_contenido_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('El campos es obligatorio')
        return value

    def validate_letra(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = OpcionEnunciado
        exclude = ('estado',)

class OpcionEnunciadoDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpcionEnunciado
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado':{
                'id': instance.id,
                'contenido_opcion': instance.contenido_enunciado,
                'letra': instance.letra
            }
        }

class JustificacionSerializer(serializers.ModelSerializer):
    afirmacion = serializers.CharField(max_length = 250)
    evidencia = serializers.CharField(max_length = 250)

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

    def validate_solucion(self, value):
        if value == '':
            raise serializers.ValdiationError('Debe seleccionar una opcion de respuesta')

    class Meta:
        model = Justificacion
        exclude = ('estado',)

class JustificacionDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Justificacion
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'justificacion':{
                'id': instance.id,
                'afirmacion': instance.afirmacion,
                'evidencia': instance.evidencia,
                'justificacion': instance.justificacion,
                'solucion': instance.solucion.id if instance.solucion.id is not None else ''
            }
        }

class PreguntaSerializer(serializers.ModelSerializer):
    def valdiate_enunciado(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def valdiate_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe existir uno(s) para la pregunta')
        return value

    def validate_respuesta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar la respuesta')
        return value

    def validate_justificacion(self, value):
        if value == '':
            raise serializers.ValidationError('Debe selecionar una justificación')
        return value

    class Meta:
        model = Pregunta
        exclude = ('estado',)

class PreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'pregunta':{
                'id': instance.id,
                'enunciado': instance.enunciado,
                'grupo': instance.grupo.id if instance.grupo.id is not None else '',
                'opcion': instance.opcion.id if instance.opcion.id is not None else '',
                'respuesta': instance.respuesta.id if instance.respuesta.id is not None else '',
                'justificacion': instance.justificacion.id if instance.justificacion.id is not None else ''
            }
        }

class BancoPreguntaSerializer(serializers.ModelSerializer):
    nombre_banco = serializers.CharField(max_length = 100)

    def validate_nombre_banco(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = BancoPregunta
        exclude = ('estado',)

class BancoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPregunta
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

class PruebaSerializer(serializers.ModelSerializer):
    nombre_prueba = serializers.CharField(max_length = 100)
    numero_intentos = serializers.IntegerField(max_length = 1)

    def validate_nombre_prueba(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_limite_tiempo(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_numero_intentos(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = Prueba
        exclude = ('estado',)

class PruebaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        exclude = ('estado')

    def to_representation(self, instance):
        banco_preguntas = BancoPregunta.objects.filter(id_referencia = isinstance.id, estado = True)
        banco_preguntas_serializer = BancoPreguntaDetalleSerializer(banco_preguntas, many = True)

        return {
            'info':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            },
            'banco_preguntas': banco_preguntas_serializer.data
        }

class ResultaddoPruebaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultadoPrueba
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'resultado_prueba':{
                'id': instance.id,
                'calificacion':instance.calificacion,
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'docente': instance.docente.id if instance.docente.id is not None else '',
                'modulo': instance.modulo.id if instance.modulo.id is not None else '',
                'prueba': instance.prueba.id if instance.prueba.id is not None else '',
                'hoja_respuesta': instance.hoja_respuesta.id if instance.hoja_respuesta.id is not None else ''
            }
        }
