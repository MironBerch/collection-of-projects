from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {
        'message': 'Hello World pushing out to ubuntu',
    }



"""
from typing import Optional
from random import randrange

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id = int
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


posts: list = []


@app.get('/')
async def hello():
    return {'hello': 'Hello world!'}


@app.get('/posts')
async def posts_list():
    return {'message': posts}


@app.post('/create')
def create_post(post: Post, status_code=status.HTTP_201_CREATED): #dict = Body(...)):
    post = post.dict()
    post['id'] = randrange(0, 1000)
    posts.append(post)
    return {
        'message': f'{post}',
    }


def find_post(id):
    for i in posts:
        if i['id'] == id:
            return i


@app.get('/posts/latest')
def get_latest_post(response: Response):
    try:
        post = posts[-1] #osts[len(posts)-1]
        return {'detail': post}
    except IndexError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.get('/posts/{id}')
async def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
    #    response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'has not post with id: { id }.'
        )
    return {'post detail': f'{post}'}


def find_index_post(id):
    for i, p in enumerate(posts):
        if p['id'] == id:
            return i


@app.delete('/posts/{id}')
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'not found',
        )
    posts.pop(index)
    return {'message': 'post deleted'}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'not found',
        )
    post_dict = post.dict()
    post_dict['id'] = id
    posts[index] = post_dict
    return {'data': post_dict}
"""
