from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .permissions import RegistrationPermission
from .serializers import RegistrationSerializer
from ..models import User


class RegistrationViewSet(mixins.CreateModelMixin, GenericViewSet):
    """Регистрация пользователя."""

    permission_classes = (RegistrationPermission,)
    queryset = User.objects.none()
    serializer_class = RegistrationSerializer
