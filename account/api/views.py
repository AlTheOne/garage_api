from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt import authentication as jwt_auth

from core.users.models import User
from .serializers import (
    SimpleCarSerializer, CarCreateSerializer, CarUpdateSerializer,
    SimpleProfileSerializer, ProfileUpdateSerializer,
)
from ..models import Car


class ProfileAPIView(APIView):
    """
    Профиль пользователя.
    """

    authentication_classes = (jwt_auth.JWTTokenUserAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Возвращаем данные пользователя.
        """

        user = get_object_or_404(User, id=request.user.id)
        serializer = SimpleProfileSerializer(user)
        return Response(data=serializer.data)

    def patch(self, request, format=None):
        """
        Частичное обновление данных пользователя.
        """

        user = get_object_or_404(User, id=request.user.id)
        serializer = ProfileUpdateSerializer(
            instance=user, data=request.data, partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CarViewSet(mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """Автомобили пользователя."""

    permission_classes = (IsAuthenticated,)
    queryset = Car.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        if self.action == 'list':
            return queryset.only(
                'car_model',
                'issue',
            )

        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return CarCreateSerializer
        elif self.action in {'update', 'partial_update'}:
            return CarUpdateSerializer

        return SimpleCarSerializer
