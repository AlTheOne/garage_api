import pytest

from specialists.models import Specialist


@pytest.fixture
def create_specialists(db):
    Specialist.objects.bulk_create([
        Specialist(
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович',
        ),
        Specialist(
            last_name='Петров',
            first_name='Петр',
            middle_name='Петрович',
        ),
        Specialist(
            last_name='Соколов',
            first_name='Сокол',
            middle_name='Соколович',
            is_active=True,
        ),
        Specialist(
            last_name='Сидоров',
            first_name='Сидр',
            middle_name='Сидорович',
            is_active=False,
        ),
    ])

    return Specialist.objects.all()
