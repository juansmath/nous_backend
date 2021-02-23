from rest_framework.routers import DefaultRouter

from apps.prueba.api.viewSets.general_viewset import ModuloViewSet, CompetenciaViewSet, OpcionRespuestaViewSet
from apps.prueba.api.viewSets.banco_pregunta_viewset import BancoPreguntaViewSet

router = DefaultRouter()

router.register(r'modulo', ModuloViewSet, basename = 'modulo')
router.register(r'competencia', CompetenciaViewSet, basename = 'competencia')
router.register(r'opcion_respuesta', OpcionRespuestaViewSet, basename = 'opcion_respuesta')
router.register(r'banco_pregunta', BancoPreguntaViewSet, basename = 'banco_pregunta')

urlpatterns = router.urls
