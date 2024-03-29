from django.db import models

# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key = True)
    estado = models.BooleanField('Estado', default = True)
    fecha_creacion = models.DateField('Fecha de creación', auto_now_add = True, auto_now = False)
    fecha_actualizacion = models.DateField('Fecha de actualizacion', auto_now_add = False, auto_now = True)
    fecha_eliminacion = models.DateField('Fecha deeliminación', auto_now_add = False, auto_now = True)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'