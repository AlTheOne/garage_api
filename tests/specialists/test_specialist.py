import pytest

from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_specialist_access(api_guest_client):
    """
    Неавторизованные опросы endpoint'ов.
    """
    url = reverse('specialist-list')
    response = api_guest_client.get(url)
    assert response.status_code == 401

    url = reverse('specialist-list')
    response = api_guest_client.post(url)
    assert response.status_code == 401

    url = reverse('specialist-detail', kwargs={'pk': 1})
    response = api_guest_client.get(url)
    assert response.status_code == 401

    url = reverse('specialist-detail', kwargs={'pk': 1})
    response = api_guest_client.put(url)
    assert response.status_code == 401

    url = reverse('specialist-detail', kwargs={'pk': 1})
    response = api_guest_client.patch(url)
    assert response.status_code == 401

    url = reverse('specialist-detail', kwargs={'pk': 1})
    response = api_guest_client.delete(url)
    assert response.status_code == 401

    url = reverse('specialist-workload')
    response = api_guest_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_specialist_list(api_auth_client, create_users, django_assert_num_queries,
                         create_specialists):
    """
    Получение списка специалистов.

    Проверяется:
        - количество запросов к БД;
        - код ответа;
        - доступны только активные;
        - определённый список полей;
    """
    url = reverse('specialist-list')

    with django_assert_num_queries(3):
        response = api_auth_client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == 3

    assert tuple(response.data['results'][0].keys()) == (
        'id', 'last_name', 'first_name', 'middle_name',
    )

    assert [item['id'] for item in response.data['results']] == [1, 2, 3]


@pytest.mark.django_db
@pytest.mark.parametrize('pk, count_qs, http_code', [
   (1, 2, 200),
   (2, 2, 200),
   (99, 2, 404),
])
def test_specialist_retrieve(pk, count_qs, http_code, api_auth_client,
                             django_assert_num_queries, create_specialists):
    """
    Получение данных специалиста.

    Проверяется:
        - количество запросов к БД;
        - код ответа;
        - доступны только активные;
        - определённый список полей;
    """
    url = reverse('specialist-detail', kwargs={'pk': pk})

    with django_assert_num_queries(count_qs):
        response = api_auth_client.get(url)

    status_code = response.status_code
    assert status_code == http_code

    if status_code == 200:
        assert tuple(response.data.keys()) == (
            'id', 'last_name', 'first_name', 'middle_name', 'date_updated',
            'date_created',
        )


@pytest.mark.django_db
def test_specialist_create_check_permissons(api_auth_client, create_specialists):
    """
    Проверка привилегий для создания.
    """
    url = reverse('specialist-list')
    response = api_auth_client.post(url, data={
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'middle_name': 'Иванович',
    })

    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    'last_name, first_name, middle_name, http_code', [
        ('Иванов', 'Иван', 'Иванович', 201),
        ('Иванов', 'Иван', '', 201),
        ('Иванов', '', '', 400),
        ('Иванов', None, None, 400),
        ('', '', None, 400),
        ('', None, 'Иванович', 400),
        ('', 'Иван', '', 400),
        (None, None, '', 400),
        (None, 'Иван', None, 400),
        (None, '', 'Иванович', 400),
])
def test_specialist_create(last_name, first_name, middle_name, http_code,
                           django_user_model, api_auth_client, create_specialists):
    """
    Создание специалиста.
    Техника: Pairwise.
    """
    user = django_user_model.objects.first()
    permission = Permission.objects.get(codename='add_specialist')
    user.user_permissions.add(permission)

    data = {}
    if last_name is not None:
        data['last_name'] = last_name
    if first_name is not None:
        data['first_name'] = first_name
    if middle_name is not None:
        data['middle_name'] = middle_name

    url = reverse('specialist-list')
    response = api_auth_client.post(url, data=data)

    status_code = response.status_code
    assert status_code == http_code

    if status_code == 201:
        assert tuple(response.data.keys()) == (
            'id', 'last_name', 'first_name', 'middle_name', 'date_updated',
            'date_created',
        )

        assert response.data['last_name'] == data['last_name']
        assert response.data['first_name'] == data['first_name']
        assert response.data['middle_name'] == data['middle_name']


@pytest.mark.django_db
def test_specialist_update_check_permissons(api_auth_client, create_specialists):
    """
    Проверка привилегий для обновления.
    """
    url = reverse('specialist-detail', kwargs={'pk': 2})

    response = api_auth_client.put(url, data={
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'middle_name': 'Иванович',
    })
    assert response.status_code == 403

    response = api_auth_client.patch(url, data={
        'first_name': 'Иван',
    })
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    'last_name, first_name, middle_name, http_code', [
        ('Иванов', 'Иван', 'Иванович', 200),
        ('Иванов', 'Иван', '', 200),
        ('Иванов', '', '', 400),
        ('Иванов', None, None, 400),
        ('', '', None, 400),
        ('', None, 'Иванович', 400),
        ('', 'Иван', '', 400),
        (None, None, '', 400),
        (None, 'Иван', None, 400),
        (None, '', 'Иванович', 400),
])
def test_specialist_update_put(last_name, first_name, middle_name, http_code,
                               django_user_model, api_auth_client, create_specialists):
    """
    Обновление данных специалиста.
    Техника Pairwise.
    """
    user = django_user_model.objects.first()
    permission = Permission.objects.get(codename='change_specialist')
    user.user_permissions.add(permission)

    data = {}
    if last_name is not None:
        data['last_name'] = last_name
    if first_name is not None:
        data['first_name'] = first_name
    if middle_name is not None:
        data['middle_name'] = middle_name

    url = reverse('specialist-detail', kwargs={'pk': 2})
    response = api_auth_client.put(url, data=data)

    status_code = response.status_code
    assert response.status_code == http_code

    if status_code == 200:
        assert tuple(response.data.keys()) == (
            'id', 'last_name', 'first_name', 'middle_name', 'date_updated',
            'date_created',
        )

        assert response.data['last_name'] == data['last_name']
        assert response.data['first_name'] == data['first_name']
        assert response.data['middle_name'] == data['middle_name']


@pytest.mark.django_db
@pytest.mark.parametrize(
    'last_name, first_name, middle_name, http_code', [
        ('Иванов', 'Иван', 'Иванович', 200),
        ('Иванов', 'Иван', '', 200),
        ('Иванов', '', '', 400),
        ('Иванов', None, None, 200),
        ('', '', None, 400),
        ('', None, 'Иванович', 400),
        ('', 'Иван', '', 400),
        (None, None, '', 200),
        (None, 'Иван', None, 200),
        (None, '', 'Иванович', 400),
])
def test_specialist_update_patch(last_name, first_name, middle_name, http_code,
                                 django_user_model, api_auth_client, create_specialists):
    """
    Частичное обновление данных специалиста.
    """
    user = django_user_model.objects.first()
    permission = Permission.objects.get(codename='change_specialist')
    user.user_permissions.add(permission)

    data = {}
    if last_name is not None:
        data['last_name'] = last_name
    if first_name is not None:
        data['first_name'] = first_name
    if middle_name is not None:
        data['middle_name'] = middle_name

    url = reverse('specialist-detail', kwargs={'pk': 2})
    response = api_auth_client.patch(url, data=data)

    status_code = response.status_code
    assert response.status_code == http_code

    if status_code == 200:
        assert tuple(response.data.keys()) == (
            'id', 'last_name', 'first_name', 'middle_name', 'date_updated',
            'date_created',
        )

        if last_name is not None:
            assert response.data['last_name'] == data['last_name']
        else:
            assert response.data['last_name'] == create_specialists[1].last_name

        if first_name is not None:
            assert response.data['first_name'] == data['first_name']
        else:
            assert response.data['first_name'] == create_specialists[1].first_name

        if middle_name is not None:
            assert response.data['middle_name'] == data['middle_name']
        else:
            assert response.data['middle_name'] == create_specialists[1].middle_name


@pytest.mark.django_db
def test_specialist_delete(django_user_model, api_auth_client, create_specialists):
    """
    Удаления записи о специалисте.
    """
    user = django_user_model.objects.first()
    permission = Permission.objects.get(codename='delete_specialist')
    user.user_permissions.add(permission)

    url = reverse('specialist-detail', kwargs={'pk': 1})

    response = api_auth_client.delete(url)
    assert response.status_code == 204

    response = api_auth_client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_specialist_workload(api_auth_client, create_specialists,
                             create_records, freezer):
    """
    Проверка загруженности специалистов.
    """

    freezer.move_to('2020-08-26T11:30:00')

    url = reverse('specialist-workload')
    response = api_auth_client.get(url)

    assert response.status_code == 200

    assert [specialist['id'] for specialist in response.data] == [1, 2, 3]
    assert [specialist['load'] for specialist in response.data] == [2.02, 1.01, 0.0]
