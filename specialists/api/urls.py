from rest_framework.routers import SimpleRouter

from .views import SpecialistViewSet

router = SimpleRouter()
router.register('', SpecialistViewSet, basename='specialist')

urlpatterns = router.urls
