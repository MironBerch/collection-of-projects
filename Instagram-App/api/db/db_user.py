from fastapi import HTTPException, status
from db.models import User
from routers.schemas import UserBase
from sqlalchemy.orm.session import Session
from db.hashing import Hash


def create_user(
    db: Session,
    request: UserBase,
):
    user = User(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(
            request.password,
        )
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_username(
    db: Session,
    username: str,
):
    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'user with username {username} not found'
        )
    
    return user