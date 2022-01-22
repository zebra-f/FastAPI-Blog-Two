from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from ..database import get_db
from .. import models, schemas
from ..utilities.b_pass import verify_password
from ..utilities.oauth2 import create_access_token


router = APIRouter(
    prefix='/login',
    tags=['Login']
)


@router.post('/', response_model=schemas.TokenResponse, status_code=status.HTTP_202_ACCEPTED)
def user_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # for now pass an email as the username in a login request form
    user = db.query(models.User).filter(models.User.email == request.username).first()
    
    if user and verify_password(request.password, user.password):
        data = {"user_id": user.id}
        access_token = create_access_token(data)
        return {
            "access_token": access_token,
            "token_type": "bearer"
                }
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail="Invalid credentials")
