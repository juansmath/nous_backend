from rest_framework import serializers
from apps.prueba.api.serializers.pregunta_serializer import PreguntaDetalleSerializer
from apps.prueba.api.serializers.general_serializer import CompetenciaSerializer, ModuloSerializer
from apps.prueba.api.serializers.grupo_pregunta_serializer import GrupoPreguntaDetalleSerializer

from apps.prueba.models import BancoPreguntas, Pregunta,GrupoPregunta, Competencia

class BancoPreguntasSerializer(serializers.ModelSerializer):
    modulo_id = serializers.IntegerField(write_only=True)
    docente_id = serializers.IntegerField(write_only=True, required=False, default=None)

    def validate_nombre_banco(self, value):
        if value == '':
            raise serializers.ValidationError('El campo es obligatorio')
        return value

    def validate_modulo(self, value):
        if value == '':
            raise serializers.ValidationError('Debe seleccionar un módulo')
        return value

    def validate_competencias(self, value):
        if value == []:
            raise serializers.ValidationError('Debe seleccionar una o más modalidades')
        return value

    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)
        depth = 1

class BancoPreguntasDetalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = BancoPreguntas
        exclude = ('estado',)

    def to_representation(self, instance):
        # preguntas = Pregunta.objects.filter(banco_preguntas = instance.id, estado = True, grupo__exact = "")
        # preguntas_serializer = PreguntaDetalleSerializer(preguntas, many = True)

        # grupos_preguntas = GrupoPregunta.objects.select_related('modulo').filter(banco_preguntas = instance.id, estado = True)
        # grupos_preguntas_serializer = GrupoPreguntaDetalleSerializer(grupos_preguntas, many = True)
        # print(grupos_preguntas.modulo)
        # modulo_serializer = ModuloSerializer(grupos_preguntas.modulo)

        return {
            'banco_pregunta':{
                'id': instance.id,
                'nombre': instance.nombre_banco,
                # 'modulo': modulo_serializer.data,
                # 'competencias': competencias_serializer.data,
            },
            # 'preguntas': preguntas_serializer.data,
            # 'grupos_preguntas': grupos_preguntas_serializer.data,
        }