import pytest

from account.models import Car


@pytest.fixture
def create_cars(db, create_users):
    return Car.objects.bulk_create([
        Car(
            car_model='Audi',
            issue=2015,
            owner=create_users[0]
        ),
        Car(
            car_model='Aston Martin',
            issue=1993,
            owner=create_users[0]
        ),
        Car(
            car_model='Tesla Model X',
            issue=2019,
            owner=create_users[1],
        ),
    ])
