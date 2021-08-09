from django.db import models
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel
from apps.estudiante.models import Estudiante
from apps.docente.models import Docente

class Modulo(BaseModel):
    nombre_modulo = models.CharField('Nombre del módulo', max_length = 100, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

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
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_competencia']
        verbose_name = 'Competencia'
        verbose_name_plural = 'Competencias'

    def __str__(self):
        return self.nombre_competencia

class NivelEjecucion(BaseModel):
    nivel = models.CharField('Nivel de desempeño', max_length = 50, null = False, blank = False)
    puntaje_minimo = models.PositiveSmallIntegerField('Puntaje minimo', null = False, blank = False)
    puntaje_maximo = models.PositiveSmallIntegerField('Puntaje maximo', null = False, blank = False)
    descripcion_general = models.TextField('Descripción nivel', null = False, blank = False)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['id']
        verbose_name = 'Nivel de desempeño'
        verbose_name_plural = 'Niveles de desempeño'

    def __str__(self):
        return self.nivel

class DescripcionNivelEjecucion(BaseModel):
    descripcion_especifica = models.TextField('Descripción especifica nivel desempeño', null = False, blank = False)
    nivel_ejecucion = models.ForeignKey(NivelEjecucion, on_delete = models.CASCADE, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['id']
        verbose_name = 'Descripcion especifica nivel de desempeño'

class NivelDificultad(BaseModel):
    nivel = models.CharField('Nivel de dificultad', max_length = 50, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['id']
        verbose_name = 'Nivel de dificultad pregunta'
        verbose_name_plural = 'Niveles de dificultad'

    def __str__(self):
        return self.nivel

class BancoPreguntas(BaseModel):
    nombre_banco = models.CharField('Nombre del banco de preguntas', max_length = 100, null = False, blank = False)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    competencia = models.OneToOneField(Competencia,on_delete = models.CASCADE, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_banco']
        managed = True
        verbose_name = 'Banco de preguntas'
        verbose_name_plural = 'Bancos de preguntas'

    def __str__(self):
        return self.nombre_banco

class GrupoPregunta(BaseModel):
    nombre_grupo = models.CharField('Nombre del grupo', max_length=200, blank=False, null=False)
    cantidad_preguntas = models.PositiveSmallIntegerField('Cantidad maxíma de preguntas', null = False, blank = False)
    banco_preguntas = models.ForeignKey(BancoPreguntas, on_delete=models.CASCADE, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_grupo']
        verbose_name = 'Grupo de preguntas'
        verbose_name_plural = 'Grupos de pregusntas'

class EnunciadoGrupoPregunta(BaseModel):
    enunciado_general = models.TextField('Enunciado general del grupo de preguntas', null = False, blank = False, unique = True)
    grupo = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE, blank=True, null=True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['fecha_creacion',]
        verbose_name = 'Enunciado grupo pregunta'
        verbose_name_plural = 'Enunciados grupo preguntas'

class OpcionRespuesta(BaseModel):
    letra_opcion = models.CharField('nombre de la letra', max_length = 1, null = False, blank = False, unique = True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['letra_opcion']
        verbose_name = 'Opcion respuesta'
        verbose_name_plural = 'Opciones respuesta'

    def __str__(self):
        return self.letra_opcion

class Justificacion(BaseModel):
    afirmacion = models.CharField('Afirmación', max_length = 250, null = False, blank = False)
    evidencia = models.CharField('Evidencia', max_length = 250, null = False, blank = False)
    justificacion = models.TextField('Justificacion de la pregunta', null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Justificacion'
        verbose_name_plural = 'Justificaciones'

class Pregunta(BaseModel):
    grupo = models.ForeignKey(GrupoPregunta, on_delete = models.CASCADE, null = True, blank = True)
    respuesta = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE, null = False, blank = False)
    justificacion = models.OneToOneField(Justificacion, on_delete = models.CASCADE, null = False, blank = False)
    banco_preguntas = models.ForeignKey(BancoPreguntas, on_delete=models.CASCADE, null = True, blank = True)
    nivel_dificultad = models.ForeignKey(NivelDificultad, on_delete=models.CASCADE, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        managed = True
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

class OpcionPregunta(BaseModel):
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
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE, blank = True, null = True)
    letra = models.CharField('Letra', max_length = 1, choices = LETRAS_OPCION, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Opcion Enunciado'
        verbose_name_plural = 'Opciones enunciado'

class EnunciadoPregunta(BaseModel):
    enunciado = models.TextField('Enunciado de la pregunta', null = False, blank = False, unique = True)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE, blank = True, null = True)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['fecha_creacion',]
        verbose_name = 'Enunciado pregunta'
        verbose_name_plural = 'Enunciados pregunta'

class ImagenEnunciadoGrupoPregunta(BaseModel):
    imagen = models.ImageField('Imagen grupo preguntas', upload_to = None, max_length=200, null = False, blank = False)
    enunciado_grupo_preguntas = models.ForeignKey(EnunciadoGrupoPregunta, on_delete = models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Imagen para grupo de preguntas'
        verbose_name_plural = 'Imagenes para grupo de preguntas'

class ImagenEnunciadoPregunta(BaseModel):
    imagen_enunciado = models.ImageField('Imagen pregunta', upload_to = None, max_length = 200)
    enunciado = models.ForeignKey(EnunciadoPregunta, on_delete = models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Imagen para pregunta'
        verbose_name_plural = 'Imagenes para preguntas'

class Prueba(BaseModel):
    nombre_prueba = models.CharField('Nombre de la prueba', max_length = 100, null = False, blank = False, unique = True)
    limite_tiempo = models.TimeField('Limite de tiempo para presentar la prueba')
    numero_intentos = models.PositiveSmallIntegerField(default = 1)
    banco_preguntas = models.ManyToManyField(BancoPreguntas)
    docente = models.ForeignKey(Docente, on_delete= models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['nombre_prueba']
        managed = True
        verbose_name = 'Prueba'
        verbose_name_plural = 'Pruebas'

    def __str__(self):
        return self.nombre_prueba

class PruebasEstudiante(BaseModel):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null = False, blank= False)
    prueba = models.ForeignKey(Prueba, on_delete = models.CASCADE, null = False, blank = False)
    presentada = models.BooleanField('Prueba presentada', default = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

class HojaRespuesta(BaseModel):
    prueba_asignada = models.ForeignKey(PruebasEstudiante, on_delete = models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, on_delete = models.CASCADE, null = True, blank = True)
    opcion_marcada = models.ForeignKey(OpcionRespuesta, on_delete = models.CASCADE, null = True, blank = True)
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    tiempo_empleado_pregunta = models.TimeField('Tiempo que empleo para responder la pregunta', null = False, blank = False)
    calificacion = models.BooleanField('Calificación pregunta', default=False, null = False, blank = False)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        verbose_name = 'Hoja de respuesta'
        verbose_name_plural = 'Hoja de respuestas'

class ResultadoPrueba(BaseModel):
    estudiante = models.ForeignKey(Estudiante, on_delete = models.CASCADE)
    docente = models.ForeignKey(Docente, on_delete = models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete = models.CASCADE)
    prueba_asignada = models.ForeignKey(PruebasEstudiante, on_delete = models.CASCADE)
    calificada = models.BooleanField('Prueba calificada', default = False, null = False, blank = False)
    numero_aciertos = models.PositiveSmallIntegerField('Respuestas correctas', null = True, blank = True)
    numero_desaciertos = models.PositiveSmallIntegerField('Respuestas incorrectas', null = True, blank = True)
    tiempo_empleado = models.TimeField('Tiempo empleado en la prueba', null = False, blank = False)
    calificacion_final = models.ForeignKey(NivelEjecucion, on_delete = models.CASCADE)
    historial = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        ordering = ['prueba_asignada', 'estudiante']
        managed = True
        verbose_name = 'Resultado de la prueba'
        verbose_name_plural = 'Resultados de las pruebas'