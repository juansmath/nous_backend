from rest_framework import serializers

from apps.prueba.models import (Modulo, Competencia, OpcionRespuesta, GrupoPregunta, EnunciadoGrupoPregunta, OpcionEnunciado,
                                Justificacion, Pregunta, EnunciadoPregunta, BancoPreguntas, Prueba, ResultadoPrueba,
                                HojaRespuesta, )

from apps.estudiante.models import Estudiante
from apps.docente.models import Docente

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
        exclude = ('estado',)

class GrupoPreguntaSerializer(serializers.ModelSerializer):
    def validate_cantidad_preguntas(self, value):
        if value == '':
            raise serializers.ValidationError('el campo es obligatorio')
        return value

    class Meta:
        model = GrupoPregunta
        exclude = ('estado',)

class GrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    pregunta = PreguntaDetalleSerializer(many = True, read_only = True)

    class Meta:
        model = GrupoPregunta
        fields = ['id','cantidad_preguntas','preguntas','fecha_creacion']


    def to_representation(self, instance):
        return {
            'grupo_preguntas':{
                'id': instance.id,
                'cantidad_preguntas': instance.cantidad_max_preguntas,
                'preguntas': self.preguntas
            }
        }

class EnunciadoGrupoPreguntaSerializer(serializers.ModelSerializer):
    def validate_enunciado_general(self, value):
        if value == '':
            raise serializers.DjangoValidationError('El campo es obligatorio')
        return value

    def validate_grupo_general(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar un grupo de preguntas')
        return value

    class Meta:
        model = EnunciadoGrupoPregunta
        exclude = ('estado',)

class EnunciadoGrupoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnunciadoGrupoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado_grupo_preguntas':{
                'id': instance.id,
                'enunciado_general': instance.enunciado_general,
                'grupo_pregunta':instance.grupo_pregunta if instance.grupo_pregunta is not None else ''
            }
        }

class OpcionEnunciadoSerializer(serializers.ModelSerializer):
    def validate_contenido_opcion(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
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
    opcion = OpcionEnunciadoSerializer(many = True, read_only = True)
    respuesta = OpcionRespuestaSerializer(many = True, read_only = True)
    justificacion = JustificacionDetalleSerializer(many = True, read_only = True)

    class Meta:
        model = Pregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'pregunta':{
                'id': instance.id,
                'enunciado': instance.enunciado,
                'grupo': instance.grupo.id if instance.grupo.id is not None else '',
                'opcion': self.opcion,
                'respuesta': self.respuesta,
                'justificacion': self.justificacion
            }
        }

class EnunciadoPreguntaSerializer(serializers.ModelSerializer):
    def valdiate_enunciado(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validation_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccioanr una pregunta')
        return value

    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado',)

class EnunciadoPreguntaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnunciadoPregunta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'enunciado_pregunta':{
                'id': instance.id,
                'enunciado': instance.enunciado,
                'pregunta': instance.pregunta if instance.pregunta is not None else ''
            }
        }

class BancoPreguntasSerializer(serializers.ModelSerializer):
    def validate_nombre_banco(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

class BancoPreguntasDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPreguntas
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
        banco_preguntas = BancoPreguntas.objects.filter(id_referencia = isinstance.id, estado = True)
        banco_preguntas_serializer = BancoPreguntasDetalleSerializer(banco_preguntas, many = True)

        return {
            'info':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            },
            'banco_preguntas': banco_preguntas_serializer.data
        }

class HojaRespuestaSerializer(serializers.ModelSerializer):
    def validate_prueba(self, value):
        if value == '':
            raise serializers.ValidationError('Debe haberse seleccionado una prueba')
        return value

    def validate_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar una pregunta')
        return value

    def validate_opcion_marcada(self, value):
        if value == '':
            raise serializers.ValidationError('Debe maracar una respuesta')
        return value

    def validate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('Estudiante no seleccionado')
        return value

    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

class HojaRespuestaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

    def to_representation(self, instance):
        return {
            'hoja_respuesta':{
                'id': instance.id,
                'prueba': instance.prueba.id if instance.prueba.id is not None else '',
                'grupo_preguntas': instance.grupo_preguntas.id if instance.grupo_preguntas.id is not None else '',
                'pregunta': instance.pregunta.id if instance.pregunta.id is not None else '',
                'opcion_marcada': instance.opcion_marcada.id if instance.opcion_marcada.id is not None else '',
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'tiempo_empleado': instance.tiempo_empleado
            }
        }

class ResultadoPruebaSerializer(serializers.ModelSerializer):
    def valdiate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionarse un estudiante')
        return value

        def validate_docente(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar el docente a cargo')
            return value

        def validate_modulo(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar un módulo')
            return value

        def validate_prueba(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar un módulo')
            return value

        def valdiate_hoja_respuesta(self, value):
            if value == '':
                raise serializers.ValidationError('Debe seleccionar la hoja de respuestas')
            return value

        class Meta:
            model = ResultadoPrueba
            exclude = ('estado',)

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
