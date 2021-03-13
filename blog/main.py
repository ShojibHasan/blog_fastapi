from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from fastapi.params import Depends
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import mode
from .database import SessionLocal, engine
from . import schemas, models
from sqlalchemy.orm import Session
from passlib.context import CryptContext

app= FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session= Depends(get_db)):
    new_blog = models.Blog(title = request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def distroy(id, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with {id} not found')

    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@app.put('/blog/{id}')
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=F"BLOG {id} not found")

    db.update(request)
    db.commit()
    return 'updated'

@app.get('/blog', response_model=List[schemas.ShowBlog])
def all(db: Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}', status_code=200)
def show(id, response: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog with the id {id} is not available')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return{'detail': f'Blog with the id {id} is not available' }
    return blog



pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post('/user',status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User,db: Session=Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name,email=request.email,password= hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user