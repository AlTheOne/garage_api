import pytest
from django.utils import timezone

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.users.models import User


@pytest.fixture
def api_guest_client():
    return APIClient()


@pytest.fixture
def create_users():
    """
    Создание пользователей.

    ВНИМАНИЕ! Функция `django.contrib.auth.hashers.make_password`
    не используется потому, что:
        1. Замедляются тесты;
        2. Авторизируемся средствами JWT (без использования пароля);
    """

    User.objects.bulk_create([
        User(
            username='user',
            email='user@user.ru',
            password='pass',
            is_active=True,
        ),
        User(
            username='test1',
            email='test1@test.ru',
            password='Password1!!!',
            is_active=True,
        ),
        User(
            username='test2',
            email='test2@test.ru',
            password='Password2!!!',
            is_active=True,
        ),
        User(
            username='test99',
            email='test99@test.ru',
            password='Password99!!!',
        ),
    ])

    return User.objects.all()


@pytest.fixture
def api_auth_client(create_users):
    client = APIClient()
    refresh = RefreshToken.for_user(create_users[0])
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    return client
