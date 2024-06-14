from .. import schemas, utils, models, oauth2
from ..database import get_db

# libary imports
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List, Optional

# initialize router
router = APIRouter(
    prefix="/posts", #set base http for each file
    tags = ["Posts"] #improves readability of documentation
)

# create post
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(user_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # database
    new_post = models.Post(user_id=current_user.id, **user_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# get all posts (v2 with votes)
@router.get("", response_model=List[schemas.PostVotesResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, search_title: Optional[str] = ""): # query parameters
    
    # database - posts and votes
    query = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
        ).join(
            models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True
        ).filter(
            models.Post.user_id == current_user.id,
            models.Post.title.ilike(f"%{search_title}%")
        ).group_by(
            models.Post.id
        )
    #print(query)
    results = query.limit(limit).all()

    return results

# get post by id - open variable at the end (order matters)
@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # database
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # status code
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    # auth
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not authorized to peform requested action.")
    
    return post

# update post by id - open variable at the end (order matters)
@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, user_post: schemas.Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # status code
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    # auth
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not authorized to peform requested action.")
    
    # update
    post_query.update(user_post.model_dump(), synchronize_session=False)
    db.commit()

    return post

# delete post by id - open variable at the end (order matters)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # status code
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    # auth
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not authorized to peform requested action.")
    
    # delete
    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)