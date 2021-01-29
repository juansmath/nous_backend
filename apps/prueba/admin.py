from django.contrib import admin
from .models import ( Modulo, Competencia, GrupoPregunta, OpcionRespuesta,
    OpcionEnunciado, Justificacion, Pregunta, BancoPregunta )

admin.site.register(Modulo)
admin.site.register(Competencia)
admin.site.register(GrupoPregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(OpcionEnunciado)
admin.site.register(Justificacion)
admin.site.register(Pregunta)
admin.site.register(BancoPregunta)
