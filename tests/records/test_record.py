from urllib.parse import urlencode

import pytest

from django.utils import timezone
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_record_access(api_guest_client):
    """
    Неавторизованные опросы endpoint'ов.
    """
    url = reverse('record-list')
    response = api_guest_client.get(url)
    assert response.status_code == 401

    url = reverse('record-list')
    response = api_guest_client.post(url)
    assert response.status_code == 401

    url = reverse('record-detail', kwargs={'pk': 1})
    response = api_guest_client.delete(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_record_list(api_auth_client, create_users, django_assert_num_queries,
                     create_record):
    """
    Получение списка записей.

    Проверяется:
        - количество запросов к БД;
        - код ответа;
        - определённый список полей;
    """
    url = reverse('record-list')

    with django_assert_num_queries(3):
        response = api_auth_client.get(url)

    assert response.status_code == 200
    assert response.data['count'] == 1

    assert tuple(response.data['results'][0].keys()) == (
        'id', 'date', 'time', 'specialist', 'is_complete',
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    'filters, response_id_list, http_code', [
        ({'date': '2020-08-24'}, [1], 200),
        ({'date__gt': '2020-08-24'}, [2, 3, 4], 200),
        ({'date__gte': '2020-08-24'}, [1, 2, 3, 4], 200),
        ({'date__lt': '2020-08-25'}, [1], 200),
        ({'date__lte': '2020-08-26'}, [1, 2, 3, 4], 200),
        ({'date': '2020-26'}, [], 400),

        ({'time': '14:00:00'}, [1, 2], 200),
        ({'time__gt': '14:00:00'}, [3, 4], 200),
        ({'time__gte': '14:00:00'}, [1, 2, 3, 4], 200),
        ({'time__lt': '15:00:00'}, [1, 2], 200),
        ({'time__lte': '15:00:00'}, [1, 2, 3, 4], 200),
        ({'time__lte': '27:00:00'}, [], 400),

        ({'date__gte': '2020-08-26', 'time__lt': '15:00:00'}, [2], 200),
        ({'date__lt': '2020-08-26', 'time': '14:00:00'}, [1], 200),
        ({'date__gte': '2020-08-24', 'time__lt': '14:00:00'}, [], 200),
        ({'date__gte': '2020-08-24', 'time__gte': '15:00:00', 'specialist_id': 1}, [3], 200),

        ({'created_by_id': 1}, [1, 2], 200),
        ({'created_by_id': 2}, [3], 200),
        ({'created_by_id': 99}, [], 400),

        ({'is_complete': True}, [1], 200),
        ({'is_complete': False}, [2, 3, 4], 200),

        ({'specialist_id': 1}, [1, 2, 3], 200),
        ({'specialist_id': 999}, [], 400),
    ])
def test_record_filter(filters, response_id_list, http_code, api_auth_client,
                       django_assert_max_num_queries, create_records):
    """
    Фильтрация списка записей.
    """
    url = reverse('record-list') + '?' + urlencode(filters)

    with django_assert_max_num_queries(4):
        response = api_auth_client.get(url)

    assert response.status_code == http_code

    if http_code == 200:
        list_id = [record['id'] for record in response.data['results']] if response.data['count'] else []
        assert list_id == response_id_list


@pytest.mark.django_db
@pytest.mark.freeze_time
@pytest.mark.parametrize(
    'day, time, specialist_id, http_code', [

        # Проверка граничных значений...
        (0, '10:00:00', 1, 400),
        (0, '9:59:59', 1, 400),
        (0, '9:00:00', 1, 400),
        (0, '20:00:00', 1, 400),
        (14, '12:00:00', 1, 201),
        (15, '12:00:00', 1, 400),
        (-1, '12:00:00', 1, 400),

        # Запись на субботу...
        (3, '12:00:00', 1, 400),

        # Некорректное время...
        (0, '15:30:00', 1, 400),

        # Pairwise
        (0, '12:00:00', 1, 201),
        (0, '', '', 400),
        (0, None, None, 400),
        ('', '', None, 400),
        ('', None, 1, 400),
        ('', '12:00:00', '', 400),
        (None, None, '', 400),
        (None, '12:00:00', None, 400),
        (None, '', 1, 400),
    ])
def test_record_create(day, time, specialist_id, http_code, api_auth_client,
                       create_specialists, freezer):
    """
    Создание заявки.

    2020-08-26 11:30:00 - Среда
    """

    freezer.move_to('2020-08-26T11:30:00')

    if day == 0 or day:
        now = timezone.now() + timezone.timedelta(days=day)
    elif day == '':
        now = ''

    data = {}
    if day is not None:
        data['date'] = now.date() if now else now
    if time is not None:
        data['time'] = time
    if specialist_id is not None:
        data['specialist'] = specialist_id

    url = reverse('record-list')
    response = api_auth_client.post(url, data=data)

    status_code = response.status_code
    assert status_code == http_code

    if status_code == 201:
        assert tuple(response.data.keys()) == (
            'id', 'date', 'time', 'specialist', 'is_complete', 'created_by',
            'date_updated', 'date_created',
        )

        assert response.data['date'] == now.date().isoformat()
        assert response.data['time'] == data['time']
        assert response.data['specialist'] == specialist_id


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_record_create_spec(api_auth_client, create_specialists,
                            create_record, freezer):
    """
    Создание заявки.
    Цель: специалист.

    2020-08-26 11:30:00 - Среда
    """

    freezer.move_to('2020-08-26T11:30:00')

    data = {
        'date': timezone.now().date(),
        'time': '12:00:00',
        'specialist': 103
    }
    url = reverse('record-list')

    # Запись к несуществующему специалисту...
    response = api_auth_client.post(url, data=data)
    assert response.status_code == 400

    # Запись на такое время уже занято...
    data['time'] = '14:00:00'
    data['specialist'] = 1
    response = api_auth_client.post(url, data=data)
    assert response.status_code == 400

    # Нельзя подать более одной заявки...
    data['time'] = '15:00:00'
    data['specialist'] = 1
    response = api_auth_client.post(url, data=data)
    assert response.status_code == 201

    data['time'] = '16:00:00'
    data['specialist'] = 2
    response = api_auth_client.post(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
@pytest.mark.freeze_time
def test_record_delete(api_auth_client, create_specialists, create_record,
                       freezer):
    """
    Удаление заявки.
    Удалять можно только свои заявки.

    2020-08-26 11:30:00 - Среда
    """

    freezer.move_to('2020-08-26T11:30:00')

    data = {
        'date': timezone.now().date(),
        'time': '15:00:00',
        'specialist': 1
    }
    url_list = reverse('record-list')
    response = api_auth_client.post(url_list, data=data)
    assert response.status_code == 201

    url_detail = reverse('record-detail', kwargs={'pk': response.data['id']})
    response = api_auth_client.delete(url_detail)
    assert response.status_code == 204

    url_detail = reverse('record-detail', kwargs={'pk': 1})
    response = api_auth_client.delete(url_detail)
    assert response.status_code == 403
