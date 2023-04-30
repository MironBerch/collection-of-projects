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


@app.get('/post/latest')
def get_latest_post(response: Response):
    try:
        post = posts[-1] #osts[len(posts)-1]
        return {'detail': post}
    except IndexError:
        response.status_code = status.HTTP_404_NOT_FOUND


@app.get('/post/{id}')
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


@app.delete('/post/del/{id}')
def delete_post(id: int):
    index = find_index_post(id)
    posts.pop(index)
    return {'message': 'post deleted'}