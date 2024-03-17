from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import Token


def validate_custom_password(password):
    try:
        validate_password(password)
        return True
    except ValidationError:
        return False


def create_token(pk) -> str:
    payload = {
        'user_id': pk,
        'exp': datetime.utcnow() + timedelta(hours=12),
    }
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm='HS256',
    )
    Token.objects.create(
        token=token,
        user_id=pk,
    )
    return token


def user_tokens_to_black(pk) -> None:
    tokens = Token.objects.filter(user_id=pk, black=False)
    for token in tokens:
        token.black = True
        token.save()


def secure_that_good_token(token, pk):
    count = Token.objects.filter(user_id=pk, black=True, token=token).count()
    return count == 0
