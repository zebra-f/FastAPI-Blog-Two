from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..utilities.b_pass import verify_password



router = APIRouter(
    prefix='/login',
    tags=['Login']
    
)


@router.post('/', status_code=status.HTTP_202_ACCEPTED)
def user_login(request: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()

    if user and verify_password(request.password, user.password):
        return {"Hello": "Grab that token"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Invalid credentials")