from rest_framework import serializers

from core.users.models import User
from ..models import Car


class SimpleProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'middle_name',
        )
        read_only_fields = fields
        extra_kwargs = {
            'first_name': {'allow_blank': False},
            'last_name': {'allow_blank': False},
        }


class ProfileUpdateSerializer(SimpleProfileSerializer):

    class Meta(SimpleProfileSerializer.Meta):
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'middle_name',
        )
        read_only_fields = ('id', 'username', 'email')

    def create(self, validated_data):
        raise serializers.ValidationError('Создание запрещено.')


class SimpleCarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = ('id', 'car_model', 'issue')
        read_only_fields = fields


class CarCreateSerializer(SimpleCarSerializer):

    class Meta(SimpleCarSerializer.Meta):
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        raise serializers.ValidationError('Обновление запрещено.')

    def validate(self, data):
        request = self.context['request']
        data['owner'] = request.user

        return data


class CarUpdateSerializer(SimpleCarSerializer):

    class Meta(SimpleCarSerializer.Meta):
        read_only_fields = ('id',)

    def create(self, validated_data):
        raise serializers.ValidationError('Создание запрещено.')
