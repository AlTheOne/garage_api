import pytest
from django.utils import timezone
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_car_access(api_guest_client):
    """
    Неавторизованные опросы endpoint'ов.
    """
    url = reverse('car-list')
    response = api_guest_client.get(url)
    assert response.status_code == 401

    url = reverse('car-list')
    response = api_guest_client.post(url)
    assert response.status_code == 401

    url = reverse('car-detail', kwargs={'pk': 1})
    response = api_guest_client.put(url)
    assert response.status_code == 401

    url = reverse('car-detail', kwargs={'pk': 1})
    response = api_guest_client.patch(url)
    assert response.status_code == 401

    url = reverse('car-detail', kwargs={'pk': 1})
    response = api_guest_client.delete(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_car_list(api_auth_client, django_assert_num_queries, create_cars):
    """
    Получение списка автомобилей пользователя.

    Проверяется:
        - количество запросов к БД;
        - код ответа;
        - определённый список полей;
        - доступны только авто пользователя;
    """
    url = reverse('car-list')

    with django_assert_num_queries(3):
        response = api_auth_client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == 2

    assert tuple(response.data['results'][0].keys()) == (
        'id', 'car_model', 'issue',
    )

    assert [item['id'] for item in response.data['results']] == [1, 2]


@pytest.mark.django_db
@pytest.mark.parametrize(
    'car_model, issue, http_code', [

        # Проверка граничных значений...
        ('Opel', 1884, 400),
        ('Opel', 1885, 201),
        ('Opel', timezone.now().year, 201),
        ('Opel', timezone.now().year - 1, 201),
        ('Opel', timezone.now().year + 1, 400),

        # Pairwise...
        ('Opel', 2015, 201),
        ('Opel', '', 400),
        ('Opel', None, 400),
        ('', '', 400),
        ('', None, 400),
        ('', 2015, 400),
        (None, None, 400),
        (None, 2015, 400),
        (None, '', 400),
    ]
)
def test_car_create(car_model, issue, http_code, api_auth_client, create_cars):
    """
    Добавления авто.
    """
    data = {}
    if car_model is not None:
        data['car_model'] = car_model
    if issue is not None:
        data['issue'] = issue

    url = reverse('car-list')
    response = api_auth_client.post(url, data=data)
    status_code = response.status_code
    assert status_code == http_code

    if status_code == 201:
        assert tuple(response.data.keys()) == ('id', 'car_model', 'issue')

        assert response.data['car_model'] == data['car_model']
        assert response.data['issue'] == data['issue']


@pytest.mark.django_db
@pytest.mark.parametrize(
    'car_model, issue, http_code', [

        # Проверка граничных значений...
        ('Opel', 1884, 400),
        ('Opel', 1885, 200),
        ('Opel', timezone.now().year, 200),
        ('Opel', timezone.now().year - 1, 200),
        ('Opel', timezone.now().year + 1, 400),

        # Pairwise...
        ('Opel', 2015, 200),
        ('Opel', '', 400),
        ('Opel', None, 400),
        ('', '', 400),
        ('', None, 400),
        ('', 2015, 400),
        (None, None, 400),
        (None, 2015, 400),
        (None, '', 400),
    ])
def test_car_update_put(car_model, issue, http_code, api_auth_client, create_cars):
    """
    Обновление данных авто.
    """
    data = {}
    if car_model is not None:
        data['car_model'] = car_model
    if issue is not None:
        data['issue'] = issue

    url = reverse('car-detail', kwargs={'pk': 1})
    response = api_auth_client.put(url, data=data)
    status_code = response.status_code
    assert status_code == http_code

    if status_code == 200:
        assert tuple(response.data.keys()) == ('id', 'car_model', 'issue')

        assert response.data['car_model'] == data['car_model']
        assert response.data['issue'] == data['issue']


@pytest.mark.django_db
@pytest.mark.parametrize(
    'car_model, issue, http_code', [

        # Проверка граничных значений...
        ('Opel', 1884, 400),
        ('Opel', 1885, 200),
        ('Opel', timezone.now().year, 200),
        ('Opel', timezone.now().year - 1, 200),
        ('Opel', timezone.now().year + 1, 400),

        # Pairwise...
        ('Opel', 2015, 200),
        ('Opel', '', 400),
        ('Opel', None, 200),
        ('', '', 400),
        ('', None, 400),
        ('', 2015, 400),
        (None, None, 200),
        (None, 2015, 200),
        (None, '', 400),
    ])
def test_car_update_patch(car_model, issue, http_code, api_auth_client, create_cars):
    """
    Частичное обновление данных авто.
    """
    data = {}
    if car_model is not None:
        data['car_model'] = car_model
    if issue is not None:
        data['issue'] = issue

    url = reverse('car-detail', kwargs={'pk': 2})
    response = api_auth_client.patch(url, data=data)
    status_code = response.status_code
    assert status_code == http_code

    if status_code == 200:
        assert tuple(response.data.keys()) == ('id', 'car_model', 'issue')

        if car_model is not None:
            assert response.data['car_model'] == data['car_model']
        else:
            assert response.data['car_model'] == create_cars[1].car_model

        if issue is not None:
            assert response.data['issue'] == data['issue']
        else:
            assert response.data['issue'] == create_cars[1].issue


@pytest.mark.django_db
def test_car_delete(api_auth_client, create_cars):
    """
    Удаление записи об авто.
    """
    url_detail = reverse('car-detail', kwargs={'pk': 1})
    response = api_auth_client.delete(url_detail)
    assert response.status_code == 204

    url_list = reverse('car-list')
    response = api_auth_client.get(url_list)
    assert [] == [car['id'] for car in response.data['results'] if car['id'] == 1]
