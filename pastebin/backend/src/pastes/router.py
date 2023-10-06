from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_config import current_active_user
from auth.models import User
from pastes.schemas import PasteCreate
from pastes.models import Paste
from database import get_async_session

router = APIRouter()


@router.post('/paste-create')
async def request_verify_email(
    paste: PasteCreate,
    user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_async_session),
):
    new_paste = Paste(
        user_id=user.id,
        title=paste.title,
        content=paste.content,
        format=paste.format,
        expire_date=paste.expire_date,
        private=paste.private,
    )
    db.add(new_paste)
    await db.commit()
    return Response(
        status_code=status.HTTP_200_OK,
    )
