from rest_framework.routers import DefaultRouter

from .api import ProgramaViewSet, FacultadViewSet, NivelAcademicoViewSet

router = DefaultRouter()

router.register(r'programa', ProgramaViewSet, basename="programas")
router.register(r'facultad', FacultadViewSet, basename="facultades")
router.register(r'nivel_academico', NivelAcademicoViewSet, basename="niveles_academicos")

urlpatterns = router.urls