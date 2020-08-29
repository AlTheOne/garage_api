import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_profile_access(api_guest_client):
    """
    Неавторизованные опросы endpoint'ов.
    """
    url = reverse('profile')
    response = api_guest_client.get(url)
    assert response.status_code == 401

    url = reverse('profile')
    response = api_guest_client.patch(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_profile(api_auth_client, create_users):
    """
    Данные профиля.
    """
    url = reverse('profile')
    response = api_auth_client.get(url)

    assert response.status_code == 200

    user = create_users[0]
    assert response.data['id'] == user.id
    assert response.data['username'] == user.username
    assert response.data['email'] == user.email
    assert response.data['first_name'] == user.first_name
    assert response.data['last_name'] == user.last_name
    assert response.data['middle_name'] == user.middle_name


@pytest.mark.django_db
@pytest.mark.parametrize(
    'last_name, first_name, middle_name, http_code', [
        ('Al', 'The', 'One', 200),
        ('Al', '', '', 400),
        ('Al', None, None, 200),
        ('', None, None, 400),
        ('', None, 'One', 400),
        ('', 'The', '', 400),
        (None, None, '', 200),
        (None, 'The', None, 200),
        (None, '', 'One', 400),
    ]
)
def test_profile_patch(last_name, first_name, middle_name, http_code,
                       api_auth_client, create_users):
    """
    Обновление данных профиля.
    """
    url = reverse('profile')
    data = {}
    if last_name is not None:
        data['last_name'] = last_name
    if first_name is not None:
        data['first_name'] = first_name
    if middle_name is not None:
        data['middle_name'] = middle_name

    response = api_auth_client.patch(url, data=data)

    status_code = response.status_code
    assert status_code == http_code

    if status_code == 200:
        if last_name is not None:
            assert response.data['last_name'] == data['last_name']
        else:
            assert response.data['last_name'] == create_users[0].last_name

        if first_name is not None:
            assert response.data['first_name'] == data['first_name']
        else:
            assert response.data['first_name'] == create_users[0].first_name

        if middle_name is not None:
            assert response.data['middle_name'] == data['middle_name']
        else:
            assert response.data['middle_name'] == create_users[0].middle_name
