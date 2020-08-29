import pytest
from rest_framework.reverse import reverse


# @pytest.mark.django_db
# def test_registration_access(api_auth_client):
#     """
#     Авторизованные опросы endpoint'ов.
#     """
#     url = reverse('registration-list')
#     response = api_auth_client.post(url)
#     assert response.status_code == 403



@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, email, password, password2, last_name, first_name, middle_name, http_code', [
        ('AlTheOne', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', 'The', 'One', 201),
        ('AlTheOne', 'email@email.com', 'ZUIY*&b87b', 'H', 'Al', 'The', 'One', 400),

        # Логин занят...
        ('user', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', 'The', 'One', 400),

        # Почта занята...
        ('AlTheOne', 'user@user.ru', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', 'The', 'One', 400),

        # Pairwise...
        ('', '', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', '', '', 400),
        (None, None, 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', None, None, 400),
        ('AlTheOne', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', '', '', None, 400),
        ('AlTheOne', '', 'ZUIY*&b87b', 'ZUIY*&b87b', '', None, 'One', 400),
        ('', None, 'ZUIY*&b87b', 'ZUIY*&b87b', '', 'The', 'One', 400),
        (None, 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', None, None, 'One', 400),
        ('AlTheOne', '', 'ZUIY*&b87b', 'ZUIY*&b87b', None, 'The', '', 400),
        ('AlTheOne', None, 'ZUIY*&b87b', 'ZUIY*&b87b', None, 'The', None, 400),
        ('', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', None, '', 'One', 400),
        ('', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', 'The', None, 400),
        ('AlTheOne', None, 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', '', 'One', 400),
        ('AlTheOne', 'email@email.com', 'ZUIY*&b87b', 'ZUIY*&b87b', 'Al', None, '', 400),
    ]
)
def test_registration(username, email, password, password2, last_name,
                      first_name, middle_name, http_code, api_guest_client,
                      create_users):
    """
    Регистрация.
    """
    url = reverse('registration-list')

    data = {}
    if username is not None:
        data['username'] = username
    if email is not None:
        data['email'] = email
    if password is not None:
        data['password'] = password
    if password2 is not None:
        data['password2'] = password2
    if last_name is not None:
        data['last_name'] = last_name
    if first_name is not None:
        data['first_name'] = first_name
    if middle_name is not None:
        data['middle_name'] = middle_name

    response = api_guest_client.post(url, data=data)

    status_code = response.status_code
    assert status_code == http_code

    if status_code == 201:
        assert tuple(response.data.keys()) == (
            'username', 'email', 'last_name', 'first_name', 'middle_name',
        )
