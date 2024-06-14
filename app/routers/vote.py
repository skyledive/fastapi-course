from .. import schemas, utils, models, oauth2
from ..database import get_db

# libary imports
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# initialize router
router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

# send vote
@router.post("", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.UserVote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # query post database to make sure post_id exists
    found_post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {vote.post_id} does not exist.")

    # query vote database for composite key
    vote_query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()

    # add vote
    if (vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post {vote.post_id}.")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        
        return {"message": "Successfully added vote."}
    
    # delete vote
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User {current_user.id} vote on {vote.post_id} does not exist.")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted vote."}