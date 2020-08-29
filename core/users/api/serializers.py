from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from ..models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(
        label='Пароль 2',
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'last_name', 'first_name', 'middle_name',
            'password', 'password2',
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'validators': [validate_password],
            },
        }

    default_error_messages = {
        'different_passwords': 'Пароли не совпадают.',
    }

    def validate(self, data):
        if data['password'] != data['password2']:
            self.fail('different_passwords')

        # HACK(AlTheOne): Сделано в демонстративных целях...
        data['is_active'] = True

        return data

    def create(self, validated_data):
        del validated_data['password2']

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user
