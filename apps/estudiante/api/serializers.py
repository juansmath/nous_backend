from rest_framework import serializers
from apps.prueba.api.serializers import PruebaDetalleSerializer, GrupoPreguntaDetalleSerializer, OpcionRespuestaSerializer, PreguntaDetalleSerializer

from apps.estudiante.models import Estudiante
from apps.prueba.models import Prueba, OpcionRespuesta, GrupoPregunta, Pregunta

class EstudianteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudiante
        fields = '__all__'