from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..utilities import oauth2


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.PostResponse], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# CREATE POST
@router.post('/', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_posts(request: schemas.CreatePost, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(
        **request.dict(), user_id = current_user.id
        # title=request.title, content=request.content, published=request.published
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@router.get('/{id}', response_model=schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")


# DELETE POST
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), 
            current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post:
        if post.user_id == current_user.id:
            post_query.delete(synchronize_session=False)
            db.commit()
        else:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to perform this operation")
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")

# UPDATE POST
@router.put('/{id}', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def update_post(id: int, request: schemas.UpdatePost, db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post:
        if post.user_id == current_user.id:
            # no need to pass an user_id to update the post
            post_query.update(request.dict(), synchronize_session=False)
            post = post_query.first()
            db.commit()
            db.refresh(post)
            return post
        else:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Not authorized to perform this operation")    

    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")



