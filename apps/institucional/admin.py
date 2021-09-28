from django.contrib import admin
from .models import Facultad, Programa, NivelAcademico, Semestre

admin.site.register(Facultad)
admin.site.register(Programa)
admin.site.register(NivelAcademico)
admin.site.register(Semestre)
