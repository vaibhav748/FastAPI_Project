from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import Token
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..utils import verify_password
from ..oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(

    tags=["Authentication"]
)

@router.post('/login', response_model=Token)
# def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid Credentials")

    # Create and return the Token
    access_token = create_access_token(data={"user_id": user.id})

    return({"access_token": access_token, "token_type": "bearer"})

## OAuth2PasswordRequestForm gives us a dict having username key and password key and we have to give data in form_data from Postman.