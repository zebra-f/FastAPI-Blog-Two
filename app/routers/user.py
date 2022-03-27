from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..utilities import oauth2
from ..utilities.b_pass import get_password_hash
from .. import models, schemas


# TODO: def get_user_profile() 
# TODO: def change_user_email()
# TODO: def change_user_password()


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get('/', response_model=List[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    
    users = db.query(models.User).all()
    return users


# CREATE USER
@router.post('/', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    
    # password requirements 
    if len(request.password) < 8:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Password should not be shorter than 8 charachters")
    elif len(request.password) > 4096:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Password should not be longer than 4096 charachters")
    
    alpha_count, digit_count, special_count = 0, 0, 0
    for char in request.password:
        if alpha_count >= 4 and digit_count >= 2 and special_count >= 1:
            break
        if char.isalpha(): alpha_count += 1
        elif char.isdigit(): digit_count += 1
        else: special_count += 1
    
    if alpha_count < 4 or digit_count < 2 or special_count < 1:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"Password should contain at least 4 letter, 2 digits and 1 special character")

    # [1/2 a] check if request.email is already taken 
    if db.query(models.User).filter(models.User.email == request.email).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail=f"This email already exists")
    # [2/2 a] if not register a new user
    else:
        request.password = get_password_hash(request.password)
        new_user = models.User(**request.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user


@router.get('/my_profile', response_model=schemas.UserMyProfileResponse, status_code=status.HTTP_200_OK)
def get_logged_user_profile(db: Session = Depends(get_db),
    current_user = Depends(oauth2.get_current_user)):

    return current_user


@router.get('/{id}', response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
            current_user = Depends(oauth2.get_current_user)):
    
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() and user_query.first() == current_user:
        user_query.delete(synchronize_session=False)
        db.commit()
    else: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user with an id = {id}")
