from django.core.exceptions import ValidationError


def validate_integer_and_positive(value):
    try:
        int_value = int(value)
        if int_value < 0:
            raise ValidationError('Value must be greater than or equal to 0.')
    except ValueError:
        raise ValidationError('Value must be an integer.')
