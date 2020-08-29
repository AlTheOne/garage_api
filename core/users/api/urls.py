from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView,
)

from .views import RegistrationViewSet


router = SimpleRouter()
router.register(
    'registration',
    RegistrationViewSet,
    basename='registration',
)

urlpatterns = [
    path(
        'token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify',
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh',
    ),
]

urlpatterns += router.urls
