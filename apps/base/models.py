from django.db import models

# Create your models here.
class BaseModel(models.Model):
    id = models.AutoField(primary_key = True)
    state = models.BooleanField('Estado', default = True)
    created_date = models.DateField('Fecha de creación', auto_now_add = True, auto_now = False)
    updated_date = models.DateField('Fecha de actualizacion', auto_now_add = False, auto_now = True)
    deleted_date = models.DateField('Fecha deeliminación', auto_now_add = False, auto_now = True)

    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base'