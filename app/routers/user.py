from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..utilities.b_pass import get_password_hash
from .. import models, schemas


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    request.password = get_password_hash(request.password)
    new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first():
        user_query.delete(synchronize_session=False)
        db.commit()
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")
