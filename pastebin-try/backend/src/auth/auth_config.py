from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy,
)

from auth.manager import get_user_manager
from auth.models import User
from config import settings

cookie_transport = CookieTransport(
    cookie_name='pastebin',
    cookie_max_age=settings.cookie_max_age,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.jwt_secret_key,
        lifetime_seconds=settings.access_token_expire_seconds,
    )


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)
current_active_verified_user = fastapi_users.current_user(
    active=True,
    verified=True,
)
