from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from api import schemas
from db import get_async_session
from models.models import Post

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_async_session)):
    posts = db.query(Post).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.Post,
    db: Session = Depends(get_async_session)):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get('/{id}', response_model=Post)
def get_post(id: int, db: Session = Depends(get_async_session)):
    post = db.query(Post).group_by(Post.id).filter(Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return post


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_async_session)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=Post)
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_async_session)):
    post_query = db.query(Post)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
