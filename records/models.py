from django.db import models

from core.users.models import User
from specialists.models import Specialist


class Record(models.Model):

    date = models.DateField(
        verbose_name='дата',
    )
    time = models.TimeField(
        verbose_name='время',
    )

    specialist = models.ForeignKey(
        verbose_name='специалист',
        to=Specialist,
        on_delete=models.CASCADE,
    )

    is_complete = models.BooleanField(
        verbose_name='выполнена',
        default=False,
    )

    created_by = models.ForeignKey(
        verbose_name='создал',
        to=User,
        on_delete=models.CASCADE,
    )

    date_updated = models.DateTimeField(
        verbose_name='обновлено',
        auto_now_add=False,
        auto_now=True,
    )
    date_created = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
        auto_now=False,
    )

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

    def __str__(self):
        return 'Заявка #{} ({})'.format(
            self.id, self.created_by.get_full_name())
