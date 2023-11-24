from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_user
from auth.jwt import (
    create_jwt_token_use_email,
    get_user_email_from_jwt_token,
    verify_jwt_token,
)
from auth.models import User
from auth.schemas import ChangePassword, ForgotPassword, ResetPassword
from auth.services import create_reset_password_link, create_verify_email_link
from auth.tasks import send_password_reset_email, send_user_verify_email
from auth.utils import get_password_hash, pwd_context
from database import get_async_session

router = APIRouter()


@router.get('/request-verify-email')
async def request_verify_email(
    user: User = Depends(current_user),
):
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


@router.post('/verify-email')
async def verify_email(
    token: str,
    db: AsyncSession = Depends(get_async_session),
):
    if not verify_jwt_token(token=token):
        raise HTTPException(
            status_code=400,
            detail='Invalid or expired token',
        )
    email = get_user_email_from_jwt_token(token=token)
    if not email:
        raise HTTPException(
            status_code=404,
            detail='Email not found',
        )
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    user.is_verified = True
    await db.merge(user)
    await db.commit()
    return Response(
        status_code=status.HTTP_200_OK,
    )


@router.post('/forgot-password')
async def forgot_password(
    request: ForgotPassword,
    db: AsyncSession = Depends(get_async_session),
):
    query = await db.execute(
        select(User).where(User.email == request.email),
    )
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='Email not found',
        )
    send_password_reset_email.delay(
        user_email=request.email,
        username=user.username,
        password_reset_link=create_reset_password_link(
            create_jwt_token_use_email(request.email),
        ),
    )
    return Response(
        status_code=status.HTTP_200_OK,
    )


@router.post('/reset-password')
async def reset_password(
    request: ResetPassword,
    token: str,
    db: AsyncSession = Depends(get_async_session),
):
    if not request.password:
        raise HTTPException(
            status_code=400,
            detail='Token not found',
        )
    if not verify_jwt_token(token=token):
        raise HTTPException(
            status_code=400,
            detail='Invalid or expired token',
        )
    email = get_user_email_from_jwt_token(token=token)
    if not email:
        raise HTTPException(
            status_code=404,
            detail='Email not found',
        )
    query = await db.execute(
        select(User).where(User.email == email),
    )
    user = query.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    user.hashed_password = get_password_hash(request.password)
    await db.merge(user)
    await db.commit()
    return Response(
        status_code=status.HTTP_200_OK,
    )


@router.post('/change-password')
async def change_password(
    request: ChangePassword,
    db: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    if not pwd_context.verify(request.old_password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail='Invalid password',
        )
    user.hashed_password = get_password_hash(request.new_password)
    await db.merge(user)
    await db.commit()
    return Response(
        status_code=status.HTTP_200_OK,
    )
