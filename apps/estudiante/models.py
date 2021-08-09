from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.persona.models import Persona
from apps.institucional.models import Programa, NivelAcademico, Semestre

class Estudiante(BaseModel):
    persona = models.OneToOneField(Persona, on_delete = models.CASCADE)
    nivel_academico = models.ForeignKey(NivelAcademico, on_delete = models.CASCADE)
    programas = models.ManyToManyField(Programa)
    semestre_id = models.ForeignKey(Semestre, on_delete = models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'