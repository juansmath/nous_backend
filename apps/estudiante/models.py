from django.db import models
from apps.base.models import BaseModel
from apps.persona.models import Persona
from apps.institucional.models import Programa, NivelAcademico

class Estudiante(BaseModel):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    nivel_academico = models.ForeignKey(NivelAcademico, on_delete = models.CASCADE)
    programas = models.ManyToManyField(Programa)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'