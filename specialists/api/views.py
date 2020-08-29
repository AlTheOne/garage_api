from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from records.models import Record
from .permissions import SpecialistPermission
from .serializers import SimpleSpecialistSerializer, SpecialistSerializer
from ..models import Specialist


class SpecialistViewSet(ModelViewSet):

    permission_classes = (IsAuthenticated, SpecialistPermission,)
    queryset = Specialist.objects.filter(is_active=True)

    def get_queryset(self):
        if self.action == 'retrieve':
            return self.queryset.only(
                'last_name',
                'first_name',
                'middle_name',
                'date_updated',
                'date_created',
            )
        elif self.action == 'list':
            return self.queryset.only(
                'last_name',
                'first_name',
                'middle_name',
            )

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleSpecialistSerializer

        return SpecialistSerializer

    @action(detail=False)
    def workload(self, request, format=None):
        """
        Загруженность специалистов на ближайшие 14 дней.

        Из 14 дней только 10 рабочих => 100 рабочих часов.
        1 запись = 1 час

        Формула загруженности специалиста (%):
            <Кол-во актуальных записей> / (100 р.ч. - <Кол-во прошедших р.ч. сегодня>) / 100%
        """
        now = timezone.now()

        data = []
        for specialist in Specialist.objects.filter(is_active=True):
            record_count = Record.objects.filter(
                date__gte=now.date(),
                specialist=specialist,
            ).exclude(
                date=now.date(),
                time__lte=now.time(),
            ).count()

            if 10 < now.hour < 20:
                old_hour = now.hour - 10
            else:
                old_hour = 0

            data.append({
                'id': specialist.pk,
                'load': round(record_count / ((100 - old_hour) / 100), 2),
            })

        return Response(data=data)
