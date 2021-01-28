from django.db import models
from apps.base.models import BaseModel

class Modulo(BaseModel):
    codigo_modulo = models.CharField('Código del módulo', max_length = 50, null = False, blank = False)
    nombre_modulo = models.CharField('Nombre del módulo', max_length = 100, null = False, blank = False)
    estado = models.BooleanField('Estado del módulo', default = True)

    class Meta:
        ordering = 'nombre_modulo'
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'

    def __str__(self):
        return self.nombre_modulo

class Competencia(BaseModel):
    nombre_competencia = models.CharField('Nombre de la competencia', max_length = 100, null = False, blank = False)
    porcentaje = models.FloatField('Porcentaje de la competencia', null = True, blank = True)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)

    class Meta:
        ordering = 'nombre_competencia'
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return self.nombre_competencia


