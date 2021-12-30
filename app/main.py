from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.param_functions import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .schemas import PostCreate, Post, UserCreate, UserOut
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from .utils import get_password_hash
from .routers import auth, post, user, vote

# Below statement will create all the tables in database.
models.Base.metadata.create_all(bind=engine)




# DataBase Connection Code


# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='FastAPI_Database', user='postgres', password='postgres',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Connected to database successfully.")
#         break
#     except Exception as error:
#         print("Connection Failed")
#         print("Error: ", error)
#         time.sleep(2)


app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)

    


# my_posts = [{"title": "My post 1", "content": "Post content 1", "id": 1}, {"title": "My post 2", "content": "Post content 2", "id": 2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i


# @app.get("/posts/")
# def get_posts():
#     return {"data": my_posts}

# @app.post("/create_posts/")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"New_post": f"title: {payload['title']} content: {payload['content']}"}

# @app.post("/posts/")
# def create_posts(post: Post):
#     print(post)
#     print(post.dict())
#     print(post.title)
    
#     return {"Data": post}

# @app.post("/create_posts/", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     post_dict = post.dict()
#     post_dict["id"] = randrange(0, 10000000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)

#     if not post:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"Message": f"Post with ID {id} not found."}
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

#     print(post)
#     return {"post_detail": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")
    
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {"data": post_dict}


# Working with Postgres DataBase...............................

# Raw query>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# @app.get("/posts/")
# def get_posts():
#     cursor.execute("SELECT * FROM posts;")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data": posts}


# @app.post("/create_posts/", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
#                   (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"data": new_post}


# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
#     post = cursor.fetchone()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

#     return {"post_detail": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")
    
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING * """,
#                         (post.title, post.content, post.published, (str(id))))
#     updated_post = cursor.fetchone()
#     conn.commit()
    
#     if updated_post == None:
        
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

    
#     return {"data": updated_post}


# SQLAlchemy Query>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# @app.get("/posts/", response_model=List[Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     # return {"data": posts}
#     return posts


# @app.post("/create_posts/", status_code=status.HTTP_201_CREATED, response_model=Post)
# def create_posts(post: PostCreate, db: Session = Depends(get_db)):
#     print(post.dict())
#     new_post = models.Post(**post.dict())
#     # new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)

#     # return {"data": new_post}
#     return new_post


# @app.get("/posts/{id}", response_model=Post)
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

#     # return {"post_detail": post}
#     return post


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")
    
#     post.delete(synchronize_session=False)
#     db.commit()
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model=Post)
# def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):

#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Post with ID {id} not found.")

#     post_query.update(updated_post.dict(), synchronize_session=False)
#     db.commit()

#     # return {"data": post_query.first()}
#     return post_query.first()


# @app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):

#     # Hash the user password.
#     hashed_password = get_password_hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user


# @app.get("/users/{id}", response_model=UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with ID {id} not found.")
    
#     return user

