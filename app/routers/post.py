from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models
from ..schemas import PostCreate, Post
from ..database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=['Posts',]
)


@router.get("/", response_model=List[Post])
def get_all_posts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user), limit:int = 10, skip:int = 0, search: Optional[str] = ""):
    # print(user_id)
    # print(type(user_id))
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # return {"data": posts}
    return posts


@router.get("/get_owner_post/{owner_id}", response_model=List[Post])
def get_owner_post(owner_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # import pdb;pdb.set_trace()

    if int(user_id.id) != owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action.")

    posts = db.query(models.Post).filter(models.Post.owner_id == owner_id).all()

    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_posts(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # print(type(user_id))
    # print(user_id.id)
    # print(post.dict())
    new_post = models.Post(owner_id = user_id.id, **post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    # return {"data": new_post}
    return new_post


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found.")

    # return {"post_detail": post}
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found.")

    print(post)
    print(post.first().owner_id)
    print(type(post.first().owner_id))
    print(user_id.id)
    print(type(user_id.id))

    if post.first().owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action.")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID {id} not found.")

    if post_query.first().owner_id != int(user_id.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized to perform requested action.")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    # return {"data": post_query.first()}
    return post_query.first()