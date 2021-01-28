from django.db import models
from apps.base.models import BaseModel
from apps.usuario.models import User

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
    identificacion = models.CharField('Número de identificación', max_length=30, null = False, blank = False, unique = True)
    primer_nombre = models.CharField('Primer nombre', max_length=100, null = False, blank = False)
    segundo_nombre = models.CharField('Segundo nombre', max_length=100, null = True, blank = True )
    primer_apellido = models.CharField('Primer apellido', max_length=100, null = False, blank = False)
    segundo_apellido = models.CharField('Segundo apellido', max_length = 100, null = True, blank = True)
    genero = models.CharField('Genéro', max_length = 4, choices = GENERO)
    rh = models.CharField('Grupo sanguineo', max_length = 3, choices = GRUPO_SANGUINEO)
    estado_civil = models.CharField('Estado civil', max_length = 15, null = False, blank = False)
    telefono = models.CharField('Número de télefono', max_length = 10, null = False, blank = False, unique = True)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null = False, blank = False)
    id_usuario = models.OneToOneField(User, on_delete = models.CASCADE )

    class Meta:
        ordering = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'

    def __str__(self):
        return f'{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}'
