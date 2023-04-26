alembic revision --autogenerate -m 'DB creation'
alembic upgrade 427006d956f3
alembic upgrade head
uvicorn main:app --reload