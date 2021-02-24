from rest_framework.routers import DefaultRouter

from .api import PersonaViewSet

router = DefaultRouter()

router.register(r'persona', PersonaViewSet, basename = 'persona')

urlpatterns = router.urls