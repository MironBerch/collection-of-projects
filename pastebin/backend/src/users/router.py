from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_user
from auth.jwt import create_jwt_token_use_email
from auth.models import User
from auth.schemas import UserEdit, UserRead
from auth.services import create_verify_email_link
from auth.tasks import send_user_verify_email
from database import get_async_session

router = APIRouter()


@router.post('/edit-user')
async def edit_user(
    request: UserEdit,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    if request.username and request.username != user.username:
        user.username = request.username
        await db.merge(user)
        await db.commit()
    if request.email and user.email != request.email:
        user.email = request.email
        user.is_verified = False
        await db.merge(user)
        await db.commit()
        send_user_verify_email.delay(
            user_email=user.email,
            username=user.username,
            verify_email_link=create_verify_email_link(
                token=create_jwt_token_use_email(
                    user_email=user.email,
                ),
            ),
        )
    return Response(
        status_code=status.HTTP_200_OK,
    )


@router.get(
    '/get-current-user',
    response_model=UserRead,
)
async def get_current_user(
    user: User = Depends(current_user),
):
    """Get the current user."""
    return user
