from celery import Celery
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.auth_config import auth_backend, fastapi_users
from auth.router import router as auth_router
from auth.schemas import UserCreate, UserRead
from config import settings
from users.router import router as users_router

celery = Celery('pastebin', broker=settings.celery_broker_url)

celery.autodiscover_tasks(['auth.tasks'])


app = FastAPI(
    title='pastebin',
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth',
    tags=['Auth'],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['Auth'],
)
app.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth'],
)
app.include_router(
    users_router,
    prefix='/users',
    tags=['Users'],
)
origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/')
async def send_hello():
    return {'Hello': 'World'}
