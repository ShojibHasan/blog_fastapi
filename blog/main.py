from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from .database import SessionLocal, engine
from . import schemas, models,hashing
from sqlalchemy.orm import Session


app= FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['blogs'])
def create(request: schemas.Blog, db: Session= Depends(get_db)):
    new_blog = models.Blog(title = request.title, body=request.body,user_id =1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT,tags=['blogs'])
def distroy(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}',tags=['blogs'])
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"BLOG {id} not found")

    db.update(request)
    db.commit()
    return 'updated'

@app.get('/blog', response_model=List[schemas.ShowBlog],tags=['blogs'])
def all(db: Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',response_model=schemas.ShowBlog, status_code=200,tags=['blogs'])
def show(id, response: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not available')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{'detail': f'Blog with the id {id} is not available' }
    return blog





@app.post('/user', response_model= schemas.ShowUser ,status_code=status.HTTP_201_CREATED, tags=['user'])
def create_user(request: schemas.User,db: Session=Depends(get_db)):
    
    new_user = models.User(name=request.name,email=request.email,password= hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user/{id}', response_model= schemas.ShowUser, tags=['user'])
def get_user(id:int,db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with the id {id} is not available')
    return user


    #  (02:35:05​) Using Doc Tags