from datetime import datetime
from sqlalchemy.orm import Session
from db.models import Comment
from routers.schemas import CommentBase


def create(
    db: Session,
    request: CommentBase,    
):
    comment = Comment(
        text = request.text,
        username = request.username,
        post_id = request.post_id,
        timestamp = datetime.now(),
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment

def get_all(
    db: Session,
    post_id: int,    
):
    return db.query(Comment).filter(
        Comment.post_id == post_id
    ).all()