from django.db import models


class Specialist(models.Model):

    last_name = models.CharField(
        verbose_name='фамилия',
        max_length=150,
    )
    first_name = models.CharField(
        verbose_name='имя',
        max_length=150,
    )
    middle_name = models.CharField(
        verbose_name='отчество',
        max_length=150,
        blank=True,
    )

    is_active = models.BooleanField(
        verbose_name='активен',
        default=True,
        help_text='Определяет видимость на сайте.',
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
        verbose_name = 'специалист'
        verbose_name_plural = 'специалисты'

    def __str__(self):
        return self.get_full_name

    @property
    def get_short_name(self):
        shot_name = '{} {}.'.format(self.last_name, self.first_name[0])
        if self.middle_name:
            shot_name += ' {}.'.format(self.middle_name)
        return shot_name

    @property
    def get_full_name(self):
        return '{} {} {}'.format(
            self.last_name, self.first_name, self.middle_name).rstrip()
