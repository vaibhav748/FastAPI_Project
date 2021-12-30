from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import Vote
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user


router = APIRouter(

    prefix="/votes",
    tags=['Vote',]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {vote.post_id} Does Not Exist.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_id.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {user_id.id} has already voted on post {vote.post_id}")

        new_vote = models.Vote(post_id = vote.post_id, user_id = user_id.id)
        db.add(new_vote)
        db.commit()
        return {"Message": "Successfully Added Vote"}
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote Does Not Exist.")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"Message": "Successfully Deleted Vote."}

