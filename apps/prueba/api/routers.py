from rest_framework.routers import DefaultRouter

from apps.prueba.api.viewSets.general_viewset import *
from apps.prueba.api.viewSets.banco_pregunta_viewset import BancoPreguntaViewSet
from apps.prueba.api.viewSets.grupo_pregunta_viewset import GrupoPreguntaViewSet
from apps.prueba.api.viewSets.pregunta_viewset import PreguntaViewSet
from apps.prueba.api.viewSets.prueba_viewset import *

router = DefaultRouter()

router.register(r'modulo', ModuloViewSet, basename = 'modulo')
router.register(r'competencia', CompetenciaViewSet, basename = 'competencia')
router.register(r'opcion_respuesta', OpcionRespuestaViewSet, basename = 'opcion_respuesta')
router.register(r'nivel_ejecucion', NivelEjecucionViewSet, basename = 'nivel_ejecucion')
router.register(r'descripcion_nivel_ejecucion', DescripcionNivelEjecucionViewSet, basename = 'descripcion_nivel_ejecucion')
router.register(r'nivel_dificultad', NivelDificultadViewSet, basename = 'nivel_dificultad')
router.register(r'banco_pregunta', BancoPreguntaViewSet, basename = 'banco_pregunta')
router.register(r'grupo_pregunta', GrupoPreguntaViewSet, basename = 'grupo_pregunta')
router.register(r'pregunta', PreguntaViewSet, basename= 'pregunta')
router.register(r'prueba', PruebaViewSet, basename= 'prueba')
router.register(r'pruebas_estudiante', PruebasEstudianteViewSet, basename= 'pruebas_estudiante')
router.register(r'resultados_pruebas', ResultadosPruebaViewSet, basename= 'resultados_pruebas')

urlpatterns = router.urls
