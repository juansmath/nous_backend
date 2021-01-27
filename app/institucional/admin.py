from django.contrib import admin
from .models import Facultad, Programa, NivelAcademico

admin.sites.register(Facultad)
admin.sites.register(Programa)
admin.sites.register(NivelAcademico)
