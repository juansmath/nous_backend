from django.db import models
from apps.base.models import BaseModel
from apps.estudiante.models import Estudiante, HojaRespuesta
from apps.docente.models import Docente

class Modulo(BaseModel):
    codigo_modulo = models.CharField('Código del módulo', max_length = 50, null = False, blank = False)
    nombre_modulo = models.CharField('Nombre del módulo', max_length = 100, null = False, blank = False)

    class Meta:
        ordering = ['nombre_modulo']
        verbose_name = 'Modulo'
        verbose_name_plural = 'Modulos'

    def __str__(self):
        return self.nombre_modulo

class Competencia(BaseModel):
    nombre_competencia = models.CharField('Nombre de la competencia', max_length = 100, null = False, blank = False)
    porcentaje = models.FloatField('Porcentaje de la competencia', null = True, blank = True)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)

    class Meta:
        ordering = ['nombre_competencia']
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return self.nombre_competencia

class GrupoPregunta(BaseModel):
    enunciado_general = models.TextField('Nombre del grupo de preguntas', null = False, blank = False)
    cantidad_max_pregutas = models.IntegerField('Cantidad maxíma de preguntas', null = False, blank = False, unique = True, max_length = 10)

    class Meta:
        ordering = ['enunciado_general']
        verbose_name = 'GrupoPregunta'
        verbose_name_plural = 'GrupoPregusntas'

    def __str__(self):
        return self.enunciado_general

class OpcionRespuesta(BaseModel):
    letra_opcion = models.CharField('nombre de la opcion', max_length = 1, null = False, blank = False, unique = True)

    class Meta:
        ordering = ['letra_opcion']
        verbose_name = 'OpcionRespuesta'
        verbose_name_plural = 'OpcionesRespuesta'

    def __str__(self):
        return self.letra_opcion

class OpcionEnunciado(BaseModel):
    LETRAS_OPCION = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('F','F'),
        ('G','G'),
        ('H','H'),
        ('I','I')
    ]
    contenido_opcion = models.CharField('Contenido de la opción', max_length = 250, null = False, blank = False, unique = True)
    letra = models.CharField('Letra', max_length = 1, choices = LETRAS_OPCION, unique = True, null = False, blank = False)

class Justificacion(BaseModel):
    afirmacion = models.CharField('Afirmación', max_length = 250, null = False, blank = False)
    evidencia = models.CharField('Evidencia', max_length = 250, null = False, blank = False)
    justificacion = models.TextField('Justificacion de la pregunta', null = False, blank = False)
    solucion = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Justificación'
        verbose_name_plural = 'Justificaciones'

class Pregunta(BaseModel):
    enunciado = models.TextField('Enunciado de la pregunta', null = False, blank = False, unique = True)
    grupo = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE)
    opcion = models.ForeignKey(OpcionEnunciado, on_delete = models.CASCADE)
    respuesta = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE)
    justificacion = models.OneToOneField(Justificacion, on_delete = models.CASCADE)

class BancoPregunta(BaseModel):
    nombre_banco = models.CharField('Nombre del banco de preguntas', max_length = 100, null = False, blank = False)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    competencia = models.ManyToManyField(Competencia)
    pregunta = models.ManyToManyField(Pregunta)
    grupo = models.ManyToManyField(GrupoPregunta)

    class Meta:
        ordering = ['nombre_banco']
        managed = True
        verbose_name = 'BancoPregunta'
        verbose_name_plural = 'BancoPreguntas'

    def __str__(self):
        return self.nombre_banco

class Prueba(BaseModel):
    nombre_prueba = models.CharField('Nombre de la prueba', max_length = 100, null = False, blank = False, unique = True)
    limite_tiempo = models.TimeField('Limite de tiempo para presentar la prueba')
    numero_intentos = models.IntegerField(max_length = 1)
    banco_preguntas = models.ManyToManyField(BancoPregunta)

    class Meta:
        ordering = ['nombre_prueba']
        managed = True
        verbose_name = 'Prueba'
        verbose_name_plural = 'Pruebas'

    def __str__(self):
        return self.nombre_prueba

class ResultadoPrueba(BaseModel):
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete = models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    prueba = models.ForeignKey(Prueba, on_delete = models.CASCADE)
    hoja_respuesta = models.ForeignKey(HojaRespuesta, on_delete = models.CASCADE)
    calificacion = models.BooleanField('Calificación de la prueba', default = False, null = False, blank = False)

    class Meta:
        ordering = ['estudiante']
        managed = True
        verbose_name = 'Resultado Prueba'
        verbose_name_plural = 'Resultados Prueba'

