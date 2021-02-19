from rest_framework.routers import DefaultRouter

from apps.prueba.api.viewSets.general_viewset import ModuloViewSet, CompetenciaViewSet, OpcionRespuestaViewSet

router = DefaultRouter()

router.register(r'modulo', ModuloViewSet, basename = 'modulo')
router.register(r'competencia', CompetenciaViewSet, basename = 'competencia')
router.register(r'opcion_respuesta', OpcionRespuestaViewSet, basename = 'opcion_respuesta')

urlpatterns = router.urls
