from django.db import models
from apps.base.models import BaseModel

class Facultad(BaseModel):
    codigo_facultad = models.CharField('Código de la facultad', max_length = 50, null = False, blank = False, unique = True)
    nombre_facultad = models.CharField('Nombre de la facultad', max_length = 100, null = False, blank = False)

    class Meta:
        ordering = ['nombre_facultad']
        verbose_name = 'Facultad'
        verbose_name_plural = 'Facultades'

    def __str__(self):
        return self.nombre_facultad

class Programa(BaseModel):
    codigo_programa = models.CharField('Código del programa', max_length=50, null = False, blank = False, unique = True)
    nombre_programa = models.CharField('Nombre del programa', max_length = 100, null = False, blank = False, unique = True)
    creditos = models.CharField('Creditos academicos del programa', max_length = 4, null = False, blank = False)
    semestres = models.CharField('Semetres', max_length = 2, null = False, blank = False)
    facultad = models.ForeignKey(Facultad, on_delete = models.CASCADE)

    class Meta:
        ordering = ['nombre_programa']
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'
        # constraints = [
        #     models.CheckConstraint(check = (creditos <= 300), name = 'creditos'),
        #     models.CheckConstraint(check = (semestres <= 20), name = 'semestres'),
        # ]

    def __str__(self):
        return self.nombre_programa

class NivelAcademico(BaseModel):
    nivel_academico = models.CharField('Nivel académico', max_length = 50, null = False, blank = False, unique = True)

    class Meta:
        ordering = ['nivel_academico']
        verbose_name = 'Nivel academico'
        verbose_name_plural = 'Niveles académicos'