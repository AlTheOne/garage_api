from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import CarViewSet, ProfileAPIView

router = SimpleRouter()
router.register(
    'cars',
    CarViewSet,
    basename='car',
)

urlpatterns = [
    path(
        '',
        ProfileAPIView.as_view(),
        name='profile',
    ),
]

urlpatterns += router.urls
