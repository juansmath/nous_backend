from django.db import models
from apps.base.models import BaseModel
from apps.persona.models import Persona
from apps.institucional.models import Programa, NivelAcademico
from apps.prueba.models import Prueba, OpcionRespuesta, GrupoPregunta, Pregunta

class Estudiante(BaseModel):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    nivel_academico = models.ForeignKey(NivelAcademico, on_delete = models.CASCADE)
    programas = models.ManyToManyField(Programa)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

class HojaRespuesta(BaseModel):
    prueba = models.ForeignKey(Prueba, on_delete = models.CASCADE)
    grupo_preguntas = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
    opcion_marcada = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE)
    estudainte = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    tiempo_empleado = models.TimeField('Tiempo que empleo para responder la pregunta', null = False, blanck = True)