from django.utils import datetime_safe, timezone
from rest_framework import serializers

from specialists.api.serializers import SimpleSpecialistSerializer
from specialists.models import Specialist
from ..models import Record


class SimpleRecordSerializer(serializers.ModelSerializer):

    specialist = SimpleSpecialistSerializer()

    class Meta:
        model = Record
        fields = ('id', 'date', 'time', 'specialist', 'is_complete')
        read_only_fields = fields


class RecordCreateSerializer(SimpleRecordSerializer):

    specialist = serializers.PrimaryKeyRelatedField(
        queryset=Specialist.objects.filter(is_active=True))

    class Meta(SimpleRecordSerializer.Meta):
        fields = (
            'id', 'date', 'time', 'specialist', 'is_complete', 'created_by',
            'date_updated', 'date_created',
        )
        read_only_fields = (
            'id', 'is_complete', 'created_by', 'date_updated', 'date_created',
        )

    ALLOW_TIME = {datetime_safe.time(hour, 0, 0) for hour in range(10, 20)}

    default_error_messages = {
        'incorrect_min_date': 'Нельзя записаться на прошедшую дату.',
        'incorrect_max_date': 'Нельзя записать позже чем на 2 недели от текущей даты.',
        'incorrect_weekday': 'Нельзя записаться на субботу/воскресенье.',
        'incorrect_time': 'Недопустимое значение.',
        'record_exist': 'Указанное время уже занято.',
        'record_limit': 'Нельзя записываться более одного раза.',
    }

    def validate_date(self, value):

        if timezone.now().date() > value:
            self.fail('incorrect_min_date')

        max_date = timezone.now() + timezone.timedelta(days=14)
        if max_date.date() < value:
            self.fail('incorrect_max_date')

        if value.isoweekday() in {6, 7}:
            self.fail('incorrect_weekday')

        return value

    def validate_time(self, value):
        if value not in self.ALLOW_TIME:
            self.fail('incorrect_time')

        return value

    def validate(self, data):

        if timezone.now().date() == data['date']:
            if timezone.now().time() > data['time']:
                self.fail('incorrect_min_date')

        user = self.context['request'].user

        if Record.objects.filter(created_by=user, is_complete=False).exists():
            self.fail('record_limit')

        if Record.objects.filter(
            date=data['date'],
            time=data['time'],
            specialist=data['specialist'],
        ).exists():
            self.fail('record_exist')

        data['created_by'] = user

        return data
