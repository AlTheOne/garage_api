from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager,
)


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_active'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    username_validator = UnicodeUsernameValidator()
    objects = UserAccountManager()

    username = models.CharField(
        verbose_name='логин',
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={'unique': 'Логин пользователя занят.'},
    )
    email = models.EmailField(
        verbose_name='почта',
        unique=True,
        blank=False,
        null=False,
    )

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

    is_staff = models.BooleanField(
        verbose_name='доступ к панели администратора',
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name='активность',
        default=False,
    )

    created = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True,
        auto_now=False,
    )
    updated = models.DateTimeField(
        verbose_name='обновлено',
        auto_now_add=False,
        auto_now=True,
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def get_short_name(self):
        shot_name = '{} {}.'.format(
            self.last_name[0] if self.last_name else '',
            self.first_name[0] if self.first_name else '',
        )
        if self.middle_name:
            shot_name += ' {}.'.format(self.middle_name[0])
        return shot_name

    def get_full_name(self):
        return '{} {} {}'.format(
            self.last_name, self.first_name, self.middle_name or '').rstrip()

    def __unicode__(self):
        return self.get_short_name()
