from django.db import models
from app.base.models import BaseModel
from app.persona.models import Persona
from app.institucional.models import Programa, NivelAcademico

class Estudiante(BaseModel):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    nivel_academico = models.ForeignKey(NivelAcademico, on_delete = models.CASCADE)
    programas = models.ManyToManyField(Programa, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'