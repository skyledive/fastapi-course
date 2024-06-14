from .. import schemas, utils, models, oauth2
from ..database import engine, get_db

# libary imports
from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# initialize router
router = APIRouter(
    prefix="/login", 
    tags=["Authentification"]
)

# login access token
@router.post('', response_model=schemas.TokenResponse)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    
    # database
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first() # OAuth2 package stores in username

    # status
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Invalid Credentials")
    
    # create token
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}