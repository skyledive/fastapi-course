from .. import schemas, utils, models, oauth2
from ..database import get_db

# libary imports
from fastapi import APIRouter, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

# initialize router
router = APIRouter(
    prefix="/users", #set base http for each file
    tags = ["Users"] #improves readability of documentation
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.User, db: Session = Depends(get_db)):

    # Check if the email already exists
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Email already registered.")

    # handle password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # database
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

# get all users
@router.get("", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):

    # database
    users = db.query(models.User).all()

    return users

# get user by id
@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # database
    user = db.query(models.User).filter(models.User.id == id).first()

    # status code
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist.")

    return user

# update user by id
@router.put("/{id}", response_model=schemas.UserOut)
def update_user(id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # database
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    # status code
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    
    # auth
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not authorized to peform requested action.")
    
    # handle password
    if user_update.password:
        hashed_password = utils.hash(user_update.password)
        user_update.password = hashed_password
    
    # update
    user_query.update(user_update.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()

    return user

# delete user by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # database
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    # status code
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist.")
    
    # auth
    if user.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User not authorized to peform requested action.")
    
    # delete
    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)