from rest_framework.routers import DefaultRouter

from apps.usuario.api.viewSets.usuario_viewset import UsuarioViewSet

router = DefaultRouter()

router.register(r'users', UsuarioViewSet, basename="usuarios")

urlpatterns = router.urls