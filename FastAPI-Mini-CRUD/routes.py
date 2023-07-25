from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .config import SessionLocal
from .schemas import Response, RequestBook
from .crud import (
    crud_create_book, crud_get_book, crud_update_book, crud_remove_book,
)


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/create')
async def create_book_service(request: RequestBook, db: Session = Depends(get_db)):
    crud_create_book(db, book=request.parameter)
    return Response(
        status='Ok',
        code='200',
        message='Book created successfully'
    ).dict(exclude_none=True)


@router.get('/')
async def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    _books = crud_get_book(db, skip, limit)
    return Response(
        status='Ok',
        code='200',
        message='Success fetch all data',
        result=_books,
    )


@router.patch('/update')
async def update_book(request: RequestBook, db: Session = Depends(get_db)):
    _book = crud_update_book(
        db,
        book_id=request.parameter.id,
        title=request.parameter.title,
        description=request.parameter.description,
    )
    return Response(
        status='Ok',
        code='200',
        message='Success update data',
        result=_book,
    )


@router.delete('/delete')
async def delete_book(request: RequestBook, db: Session = Depends(get_db)):
    crud_remove_book(db, book_id=request.parameter.id)
    return Response(
        status='Ok',
        code='200',
        message='Success delete data',
    ).dict(exclude_none=True)
