
from fastapi import status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import UserCreate, UserOut
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..utils import get_password_hash
from sqlalchemy import literal

router = APIRouter(
    prefix="/users",
    tags=['Users']
)   


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    q = db.query(models.User).filter(models.User.email == user.email)
    email_exists = db.query(literal(True)).filter(q.exists()).scalar()
    print(email_exists)

    if email_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User with Email {user.email} already exists.")

    # Hash the user password.
    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with ID {id} not found.")
    
    return user
