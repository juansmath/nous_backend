from django.contrib import admin
from .models import ( Modulo, Competencia, NivelEjecucion, DescripcionNivelEjecucion, NivelDificultad, GrupoPregunta,
                     EnunciadoGrupoPregunta, OpcionRespuesta, OpcionPregunta, Justificacion, Pregunta, EnunciadoPregunta,
                     ImagenEnunciadoGrupoPregunta, ImagenEnunciadoPregunta, BancoPreguntas, Prueba, HojaRespuesta,
                     ResultadoPrueba)

admin.site.register(Modulo)
admin.site.register(Competencia)
admin.site.register(NivelEjecucion)
admin.site.register(DescripcionNivelEjecucion)
admin.site.register(NivelDificultad)
admin.site.register(GrupoPregunta)
admin.site.register(EnunciadoGrupoPregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(OpcionPregunta)
admin.site.register(Justificacion)
admin.site.register(Pregunta)
admin.site.register(EnunciadoPregunta)
admin.site.register(ImagenEnunciadoGrupoPregunta)
admin.site.register(ImagenEnunciadoPregunta)
admin.site.register(BancoPreguntas)
admin.site.register(Prueba)
admin.site.register(HojaRespuesta)
admin.site.register(ResultadoPrueba)
