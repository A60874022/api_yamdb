from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year:
        return ValidationError('Такого года не существует')