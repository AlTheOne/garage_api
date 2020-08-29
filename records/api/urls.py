from rest_framework.routers import SimpleRouter

from records.api.views import RecordViewSet

router = SimpleRouter()
router.register('', RecordViewSet, basename='record')

urlpatterns = router.urls
