from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .filters import RecordFilter
from .permissions import RecordPermission
from .serializers import SimpleRecordSerializer, RecordCreateSerializer
from ..models import Record


class RecordViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):

    permission_classes = (IsAuthenticated, RecordPermission,)
    queryset = Record.objects.all()
    filterset_class = RecordFilter

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.select_related(
                'specialist',
            ).only(
                'date',
                'time',
                'specialist_id',
                'specialist__last_name',
                'specialist__first_name',
                'specialist__middle_name',
                'is_complete',
            )

        return self.queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return RecordCreateSerializer

        return SimpleRecordSerializer
