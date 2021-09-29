from rest_framework import serializers

from apps.prueba.api.serializers.banco_pregunta_serializer import BancoPreguntasDetalleSerializer
from apps.prueba.api.serializers.general_serializer import ModuloSerializer, NivelEjecucionSerializer
from apps.docente.api.serializers import DocenteSerializer
from apps.estudiante.api.serializers import EstudianteSerializer

from apps.prueba.models import Prueba, HojaRespuesta, BancoPreguntas, Modulo, NivelEjecucion, PruebasEstudiante
from apps.estudiante.models import Estudiante
from apps.docente.models import Docente

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

    def to_representation(self, instance):
        return {
            'prueba':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            }
        }

class PruebaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prueba
        exclude = ('estado')

    def to_representation(self, instance):
        banco_preguntas = BancoPreguntas.objects.filter(id = instance.banco_preguntas, estado = True)
        banco_preguntas_serializer = BancoPreguntasDetalleSerializer(banco_preguntas, many = True)

        docente = Docente.objects.filter(id = instance.docente, estado = True).first()
        docente_serializer = DocenteSerializer(docente)

        return {
            'pregunta':{
                'id': instance.id,
                'nombre_prueba': instance.nombre_prueba,
                'numero_intentos': instance.numero_intentos,
                'limite_tiempo': instance.limite_tiempo
            },
            'banco_preguntas': banco_preguntas_serializer.data,
            'docente': docente_serializer.data
        }

class PruebaEstudianteSerializer(serializers.ModelSerializer):
    def validate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_docente(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_prueba(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_modulo(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    class Meta:
        model = PruebasEstudiante
        exclude = ('estado',)

class PruebaEstudianteDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PruebasEstudiante
        exclude = ('estado',)

    def to_representation(self, instance):
        prueba = Prueba.objects.filter(id = instance.prueba, estado = True).first()
        prueba_serializer = PruebaSerializer(prueba)

        estudiante = Estudiante.objects.filter(id = instance.estudiante, estado=True).select_related('persona')
        estudiante_serializer = EstudianteSerializer(estudiante)

        nivel_ejecucion = NivelEjecucion.objects.filter(id = instance.nivel_ejecucion, estado=True).first()
        nivel_ejecucion_serializer = NivelEjecucionSerializer(nivel_ejecucion)

        return {
            'id': instance.id,
            'prueba': prueba_serializer.data,
            'estudiante': estudiante_serializer.data,
            'presentada': instance.presentada,
            'calificada': instance.calificada,
            'numero_aciertos': instance.numero_aciertos,
            'numero_desaciertos': instance.numero_desaciertos,
            'tiempo_empleado': instance.tiempo_empleado,
            'puntaje_prueba': instance.puntaje_prueba,
            'nivel_ejecucion': nivel_ejecucion_serializer.data
        }

class HojaRespuestaSerializer(serializers.ModelSerializer):
    def validate_prueba_asignada(self, value):
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

    def validate_tiempo_empleado_pregunta(self, value):
        if value == '':
            raise serializers.ValidationError('Debe agregarse el tiempo para la pregunta')
        return value

    def validate_estudiante(self, value):
        if value == '':
            raise serializers.ValidationError('Estudiante no seleccionado')
        return value

    def validate_nota(self, value):
        if value == '':
            raise serializers.ValidationError('Se debe de calificar la prueba')
        return value

    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

class HojaRespuestaDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HojaRespuesta
        exclude = ('estado',)

    def to_representation(self, instance):
        opcion_marcada = OpcionRespuesta.objects.filter(id = instance.opcion_marcada)
        opcion_marcada_serializer = OpcionRespuestaSerializer(opcion_marcada, many = True)

        return {
            'hoja_respuesta':{
                'id': instance.id,
                'prueba_asignada': instance.prueba_asignada.id if instance.prueba_asignada.id is not None else '',
                'pregunta': instance.pregunta.id if instance.pregunta.id is not None else '',
                'opcion_marcada': opcion_marcada_serializer.data,
                'estudiante': instance.estudiante.id if instance.estudiante.id is not None else '',
                'tiempo_empleado_pregunta': instance.tiempo_empleado_pregunta,
                'calificada': instance.calificada
            }
        }

