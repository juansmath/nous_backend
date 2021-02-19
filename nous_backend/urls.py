from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path('institucional/', include('apps.institucional.api.urls')),
    re_path('prueba/', include('apps.prueba.api.urls')),
]
