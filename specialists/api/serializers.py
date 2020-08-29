from rest_framework import serializers

from ..models import Specialist


class SimpleSpecialistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialist
        fields = ('id', 'last_name', 'first_name', 'middle_name')
        read_only_fields = fields


class SpecialistSerializer(SimpleSpecialistSerializer):

    class Meta(SimpleSpecialistSerializer.Meta):
        fields = (
            'id', 'last_name', 'first_name', 'middle_name', 'date_updated',
            'date_created',
        )
        read_only_fields = ('id', 'date_updated', 'date_created')
