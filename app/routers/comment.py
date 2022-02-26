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


@router.get('/{id}/comments', status_code=status.HTTP_200_OK)
def get_comments(id: int, request: schemas.CreateComment, db: Session = Depends(get_db)):

    pass


@router.get('/{id}/comments', status_code=status.HTTP_201_CREATED)
def create_comment(id: int, request: schemas.CreateComment, db: Session = Depends(get_db),
            current_user = Depends(oauth2.get_current_user)):

    pass



