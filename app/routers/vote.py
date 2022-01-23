from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..utilities import oauth2


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(request: schemas.Vote, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == request.post_id, models.Vote.user_id == current_user.id)

    if request.dir == 1:
        if vote_query.first():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="user has already voted")
        else:
            new_vote = models.Vote(post_id = request.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
    
    else:
        if vote_query.first():
            vote_query.delete(synchronize_session=False)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail="can't perform this action, vote not found")