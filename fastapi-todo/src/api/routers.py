from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update

from api import schemas
from db import get_async_session
from models.models import Post

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=list[schemas.Post])
async def get_posts(db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Post))
    posts = result.scalars().all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_posts(post: schemas.Post, db: AsyncSession = Depends(get_async_session)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=schemas.Post)
async def get_post(id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await db.delete(post)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post