from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(year):
    if year > timezone.now().year or year < 1945:
        return ValidationError('Не может быть опубликовано')
