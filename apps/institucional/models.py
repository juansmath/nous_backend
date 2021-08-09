from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel

class Facultad(BaseModel):
    nombre_facultad = models.CharField('Nombre de la facultad', max_length = 100, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_facultad']
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'

    def __str__(self):
        return self.nombre_facultad

class Semestre(BaseModel):
    semestre = models.CharField('Semestre', max_length=100, unique=True, null=False, blank=False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['semestre']
        verbose_name = 'Semestre'
        verbose_name_plural = 'Semestres'

    def __str__(self):
        return self.semestre or ''

class Programa(BaseModel):
    nombre_programa = models.CharField('Nombre del programa', max_length = 100, null = False, blank = False, unique = True)
    creditos = models.PositiveSmallIntegerField('Creditos academicos del programa', null = False, blank = False)
    semestres = models.PositiveSmallIntegerField('Semetres', null = False, blank = False)
    facultad = models.ForeignKey(Facultad, on_delete = models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_programa']
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'

    def __str__(self):
        return self.nombre_programa

class NivelAcademico(BaseModel):
    nivel_academico = models.CharField('Nivel académico', max_length = 50, null = False, blank = False, unique = True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nivel_academico']
        verbose_name = 'Nivel academico'
        verbose_name_plural = 'Niveles académicos'

    def __str__(self):
        return self.nivel_academico