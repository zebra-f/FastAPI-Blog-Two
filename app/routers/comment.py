from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..utilities import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)

# id refers to the post id 
# c_id refers to the comment id

# TODO: query check if post (id) exists 
@router.get('/{id}/comments', response_model=List[schemas.CommentResponse], status_code=status.HTTP_200_OK)
def get_comments(id: int, db: Session = Depends(get_db)):

    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()
    
    return comments


@router.get('/{id}/comments/{c_id}', response_model=schemas.CommentResponse, status_code=status.HTTP_200_OK)
def get_comment(id: int, c_id: int, db: Session = Depends(get_db)):

    comment = db.query(models.Comment).filter(
        models.Comment.post_id == id, models.Comment.id == c_id).first()

    if comment:
        return comment
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment or post doesn't exist")


# CREATE COMMENT
@router.post('/{id}/comments', status_code=status.HTTP_201_CREATED)
def create_comment(id: int, request: schemas.CreateComment, db: Session = Depends(get_db),
            current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:

        new_comment = models.Comment(
            **request.dict(), post_id = id, user_id = current_user.id
        )

        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        return new_comment
    
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"No post with id = {id}")



