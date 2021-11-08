from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from apps.base.views import Login, Logout
from apps.usuario.api.viewSets.usuario_viewset import RegisterView

schema_view = get_schema_view(
   openapi.Info(
      title="NOUS API RESTFUL DOCUMENTACIÓN",
      default_version='v1',
      description="Rutas para cada uno de los módelos involucrados dentro del desarrollo de la API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="juansejunior10@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuario.api.urls')),
    path('login', Login.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register_user'),
    path('logout', Logout.as_view(), name='logout'),
    path('institucional/', include('apps.institucional.api.urls')),
    path('pruebas/', include('apps.prueba.api.routers')),
    path('personas/', include('apps.persona.api.router')),
]
