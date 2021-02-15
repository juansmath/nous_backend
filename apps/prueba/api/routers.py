from rest_framework.routers import DefaultRouter

from apps.prueba.api.viewSets.general_viewset import ModuloViewSet, CompetenciaViewSet, OpcionRespuestaViewSet

router = DefaultRouter()

router.register(r'prueba/modulo', ModuloViewSet, basename = 'modulo')
router.register(r'prueba/competencia', CompetenciaViewSet, basename = 'competencia')
router.register(r'prueba/opcion_respuesta', OpcionRespuestaViewSet, basename = 'opcion_respuesta')


