import pytest
from django.utils import timezone

from records.models import Record


@pytest.fixture
def create_record(db, create_users, create_specialists):
    return Record.objects.create(
        date=timezone.now().date().replace(year=2020, month=8, day=26),
        time=timezone.now().time().replace(
            hour=14, minute=0, second=0, microsecond=0),
        specialist=create_specialists[0],
        created_by=create_users[1],
    )


@pytest.fixture
def create_records(db, create_users, create_specialists):
    Record.objects.bulk_create([
        Record(
            date=timezone.now().date().replace(year=2020, month=8, day=24),
            time=timezone.now().time().replace(
                hour=14, minute=0, second=0, microsecond=0),
            specialist=create_specialists[0],
            is_complete=True,
            created_by=create_users[0],
        ),
        Record(
            date=timezone.now().date().replace(year=2020, month=8, day=26),
            time=timezone.now().time().replace(
                hour=14, minute=0, second=0, microsecond=0),
            specialist=create_specialists[0],
            created_by=create_users[0],
        ),
        Record(
            date=timezone.now().date().replace(year=2020, month=8, day=26),
            time=timezone.now().time().replace(
                hour=15, minute=0, second=0, microsecond=0),
            specialist=create_specialists[0],
            created_by=create_users[1],
        ),
        Record(
            date=timezone.now().date().replace(year=2020, month=8, day=26),
            time=timezone.now().time().replace(
                hour=15, minute=0, second=0, microsecond=0),
            specialist=create_specialists[1],
            created_by=create_users[2],
        ),
    ])

    return Record.objects.all()
