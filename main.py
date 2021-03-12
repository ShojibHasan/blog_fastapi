from typing import Optional, Text
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn


app = FastAPI()

@app.get('/blog')
def index(limit=10,published:bool=True, sort: Optional[str] = None):
    if published:

        return {'data': f'{limit} published blog list '}
    else:
        return {'data': f'{limit} unpublished blog list '}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}')
def show(id: int):
    return {'data': id}



@app.get('/blog/{id}/comments')
def comments(id, limit=10):
    return {'data': {'1','2'}}


class Blog(BaseModel):
    title: str
    body: str
    published : Optional[bool]

@app.post('/blog')
def create_blog(request: Blog):
    return request
    # return {'data': "Blog is Created"}

#  