from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_range_issue(value: int) -> None:
    """
    Валидация года выпуска автомобиля:
        - не старше первого выпущенного автомобиля;
        - не из будущего.

    :param value: Год выпуска.
    :type value: int
    """

    if value < 1885 or value > timezone.now().year:
        raise ValidationError('Указано некорректное значение.')
