from rest_framework import serializers
from apps.docente.models import Docente

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = '__all__'