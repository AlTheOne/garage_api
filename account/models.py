from django.db import models

from core.users.models import User
from .validators import validate_range_issue


class Car(models.Model):

    car_model = models.CharField(
        verbose_name='марка',
        max_length=256,
    )
    issue = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        validators=[validate_range_issue],
    )

    owner = models.ForeignKey(
        verbose_name='владелец',
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
        verbose_name = 'автомобиль'
        verbose_name_plural = 'автомобили'

    def __str__(self):
        return self.car_model[:50]
