import django_filters

from ..models import Record


class RecordFilter(django_filters.FilterSet):

    class Meta:
        model = Record
        fields = {
            'date': ('exact', 'lt', 'gt', 'lte', 'gte'),
            'time': ('exact', 'lt', 'gt', 'lte', 'gte'),
            'specialist_id': ('exact',),
            'is_complete': ('exact',),
            'created_by_id': ('exact',),
        }
