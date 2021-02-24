from django.db import models
# from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.estudiante.models import Estudiante
from apps.docente.models import Docente

class Modulo(BaseModel):
    codigo_modulo = models.CharField('Código del módulo', max_length = 50, null = False, blank = False)
    nombre_modulo = models.CharField('Nombre del módulo', max_length = 100, null = False, blank = False)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

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
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['nombre_competencia']
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return self.nombre_competencia

class GrupoPregunta(BaseModel):
    cantidad_preguntas = models.PositiveSmallIntegerField('Cantidad maxíma de preguntas', null = False, blank = False, unique = True)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['cantidad_preguntas']
        verbose_name = 'Grupo de preguntas'
        verbose_name_plural = 'Grupos de pregusntas'

class EnunciadoGrupoPregunta(BaseModel):
    enunciado_general = models.TextField('Enunciado de la pregunta', null = False, blank = False, unique = True)
    grupo_pregunta = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['fecha_creacion',]
        verbose_name = 'Enunciado grupo pregunta'
        verbose_name_plural = 'Enunciados grupo preguntas'

class OpcionRespuesta(BaseModel):
    letra_opcion = models.CharField('nombre de la opcion', max_length = 1, null = False, blank = False, unique = True)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['letra_opcion']
        verbose_name = 'Opcion respuesta'
        verbose_name_plural = 'Opciones respuesta'

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
        ('I','I'),
        ('J','J'),
        ('K','K'),
        ('L','L'),
        ('M','M'),
        ('N','N'),
        ('O','O'),
        ('P','P'),
    ]
    contenido_opcion = models.CharField('Contenido de la opción', max_length = 250, null = False, blank = False, unique = True)
    letra = models.CharField('Letra', max_length = 1, choices = LETRAS_OPCION, unique = True, null = False, blank = False)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
        # self.changed_by = value

    class Meta:
        verbose_name = 'Opcion Enunciado'
        verbose_name_plural = 'Opciones enunciado'


class Justificacion(BaseModel):
    afirmacion = models.CharField('Afirmación', max_length = 250, null = False, blank = False)
    evidencia = models.CharField('Evidencia', max_length = 250, null = False, blank = False)
    justificacion = models.TextField('Justificacion de la pregunta', null = False, blank = False)
    solucion = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        verbose_name = 'Justificacion'
        verbose_name_plural = 'Justificaciones'

class Pregunta(BaseModel):
    grupo = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE, null = True, blank = True)
    opcion = models.ForeignKey(OpcionEnunciado, on_delete = models.CASCADE)
    respuesta = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE)
    justificacion = models.OneToOneField(Justificacion, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        managed = True
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

class EnunciadoPregunta(BaseModel):
    enunciado = models.TextField('Enunciado de la pregunta', null = False, blank = False, unique = True)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['fecha_creacion',]
        verbose_name = 'Enunciado pregunta'
        verbose_name_plural = 'Enunciados pregunta'

class ImagenEnunciadoGrupoPregunta(BaseModel):
    imagen = models.ImageField('Imagen grupo preguntas', upload_to = None, max_length=200, null = False, blank = False)
    enunciado_grupo_preguntas = models.ForeignKey(EnunciadoGrupoPregunta, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        verbose_name = 'Imagen para grupo de preguntas'
        verbose_name_plural = 'Imagenes para grupo de preguntas'

class ImagenEnunciadoPregunta(BaseModel):
    imagen_enunciado = models.ImageField('Imagen pregunta', upload_to = None, max_length = 200)
    enunciado = models.ForeignKey(EnunciadoPregunta, on_delete = models.CASCADE)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        verbose_name = 'Imagen para pregunta'
        verbose_name_plural = 'Imagenes para preguntas'

class BancoPreguntas(BaseModel):
    nombre_banco = models.CharField('Nombre del banco de preguntas', max_length = 100, null = False, blank = False)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    competencia = models.ManyToManyField(Competencia)
    pregunta = models.ManyToManyField(Pregunta, null = True, blank = True)
    grupo_pregunta = models.ManyToManyField(GrupoPregunta)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['nombre_banco']
        managed = True
        verbose_name = 'Banco de preguntas'
        verbose_name_plural = 'Bancos de preguntas'

    def __str__(self):
        return self.nombre_banco

class Prueba(BaseModel):
    nombre_prueba = models.CharField('Nombre de la prueba', max_length = 100, null = False, blank = False, unique = True)
    limite_tiempo = models.TimeField('Limite de tiempo para presentar la prueba')
    numero_intentos = models.PositiveSmallIntegerField(default = 1)
    banco_preguntas = models.ManyToManyField(BancoPreguntas)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['nombre_prueba']
        managed = True
        verbose_name = 'Prueba'
        verbose_name_plural = 'Pruebas'

    def __str__(self):
        return self.nombre_prueba

class HojaRespuesta(BaseModel):
    prueba = models.ForeignKey(Prueba, on_delete = models.CASCADE)
    grupo_preguntas = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE, null = True, blank = True)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE, null = True, blank = True)
    opcion_marcada = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE, null = True, blank = True)
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    tiempo_empleado = models.TimeField('Tiempo que empleo para responder la pregunta', null = False, blank = False)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        verbose_name = 'Hoja de respuesta'
        verbose_name_plural = 'Hoja de respuestas'

class ResultadoPrueba(BaseModel):
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete = models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    prueba = models.ForeignKey(Prueba, on_delete = models.CASCADE)
    hoja_respuesta = models.ForeignKey(HojaRespuesta, on_delete = models.CASCADE)
    calificacion = models.BooleanField('Calificación de la prueba', default = False, null = False, blank = False)
    # historial = HistoricalRecords()

    # @property
    # def _history_user(self):
    #     return self.changed_by

    # @_history_user_.setter
    # def _history_user(self, value):
    #     self.changed_by = value

    class Meta:
        ordering = ['estudiante']
        managed = True
        verbose_name = 'Resultado de la prueba'
        verbose_name_plural = 'Resultados de las pruebas'