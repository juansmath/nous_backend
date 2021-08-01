from django.db import models
# from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.usuario.models import Usuario

class Persona(BaseModel):
    GENERO = [
        ('F','FEMENINO'),
        ('M','MASCULINO'),
        ('LGTIB','LGTIB')
    ]
    ESTADO_CIVIL = [
        ('SOLTERO','SOLTERO(A)'),
        ('CASADO','CASADO'),
        ('DIVORCIADO','DIVORCIADO(A)'),
        ('VIUDO','VIUDO(A)'),
        ('UNION_LIBRE','UNION_LIBRE')
    ]
    GRUPO_SANGUINEO = [
        ('A+','A+'),
        ('A-','A-'),
        ('B+', 'B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-')
    ]
    identificacion = models.PositiveIntegerField('Número de identificación', null = False, blank = False, unique = True)
    primer_nombre = models.CharField('Primer nombre', max_length=100, null = False, blank = False)
    segundo_nombre = models.CharField('Segundo nombre', max_length=100, null = True, blank = True )
    primer_apellido = models.CharField('Primer apellido', max_length=100, null = False, blank = False)
    segundo_apellido = models.CharField('Segundo apellido', max_length = 100, null = True, blank = True)
    genero = models.CharField('Genéro', choices = GENERO, max_length = 6)
    rh = models.CharField('Grupo sanguineo', max_length = 3, choices = GRUPO_SANGUINEO)
    estado_civil = models.CharField('Estado civil', max_length = 15, null = False, blank = False, choices = ESTADO_CIVIL)
    telefono = models.CharField('Número de télefono', null = False, blank = False, unique = True, max_length = 50)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null = False, blank = False)
    usuario = models.OneToOneField(Usuario, on_delete = models.CASCADE )
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
        # self.changed_by = value

    class Meta:
        ordering = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.primer_nombre} {self.segundo_nombre or ""} {self.primer_apellido} {self.segundo_apellido or ""}'
