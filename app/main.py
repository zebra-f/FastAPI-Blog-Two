from fastapi import FastAPI, Body, status, HTTPException, Depends
from typing import List

from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db


models.Base.metadata.create_all(bind=engine)




app = FastAPI()



@app.get('/posts', response_model=List[schemas.PostResponse], status_code=status.HTTP_200_OK)
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_posts(request: schemas.CreatePost, db: Session = Depends(get_db)):
    new_post = models.Post(
        **request.dict()
        # title=request.title, content=request.content, published=request.published
        )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post


@app.get('/posts/{id}', response_model=schemas.PostResponse, status_code=status.HTTP_200_OK)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post:
        return post
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first():
        post_query.delete(synchronize_session=False)
        db.commit()
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")


@app.put('/posts/{id}', response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def update_post(id: int, request: schemas.UpdatePost, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first():
        post_query.update(request.dict(), synchronize_session=False)
        post = post_query.first()
        db.commit()
        db.refresh(post)
        return post
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with an id = {id}")


@app.get('/users', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.post('/users', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first():
        user_query.delete(synchronize_session=False)
        db.commit()
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")


