import datetime

from jwt.api_jwt import decode, encode
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidTokenError,
)

from config import settings


def create_jwt_token_use_email(user_email: str):
    """Create jwt token use user email."""
    payload: dict[str] = {
        'email': user_email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = encode(
        payload,
        settings.jwt_secret_key,
        algorithm='HS256',
    )
    return token


def verify_jwt_token(token: str) -> bool:
    """Verify jwt token."""
    try:
        payload = decode(token, settings.jwt_secret_key, algorithms=['HS256'])
        expiration_time = datetime.datetime.fromtimestamp(payload['exp'])
        if expiration_time < datetime.datetime.utcnow():
            return False
        return True
    except InvalidTokenError or ExpiredSignatureError:
        return False


def get_user_email_from_jwt_token(token: str) -> str | None:
    """Get user email from jwt token."""
    try:
        payload = decode(token, settings.jwt_secret_key, algorithms=['HS256'])
        user_email = payload['email']
        return user_email
    except ExpiredSignatureError or DecodeError or InvalidTokenError:
        return None
