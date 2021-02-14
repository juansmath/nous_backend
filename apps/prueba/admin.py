from django.contrib import admin
from .models import ( Modulo, Competencia, GrupoPregunta, EnunciadoGrupoPregunta, OpcionRespuesta,
    OpcionEnunciado, Justificacion, Pregunta, EnunciadoPregunta, ImagenEnunciadoGrupoPregunta, ImagenEnunciadoPregunta,
    BancoPreguntas, Prueba, HojaRespuesta, ResultadoPrueba)

admin.site.register(Modulo)
admin.site.register(Competencia)
admin.site.register(GrupoPregunta)
admin.site.register(EnunciadoGrupoPregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(OpcionEnunciado)
admin.site.register(Justificacion)
admin.site.register(Pregunta)
admin.site.register(EnunciadoPregunta)
admin.site.register(ImagenEnunciadoGrupoPregunta)
admin.site.register(ImagenEnunciadoPregunta)
admin.site.register(BancoPreguntas)
admin.site.register(Prueba)
admin.site.register(HojaRespuesta)
admin.site.register(ResultadoPrueba)
