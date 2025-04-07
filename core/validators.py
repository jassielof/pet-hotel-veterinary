from django.core.exceptions import ValidationError
from datetime import date


def validateNonNegative(value):
    if value <= 0:
        raise ValidationError("El peso no puede ser negativo.")


def validatePastDate(value):
    if value > date.today():
        raise ValidationError("La fecha no puede ser futura.")
