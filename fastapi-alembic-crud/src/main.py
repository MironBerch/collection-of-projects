import uvicorn

import schemas
import models
from database import get_async_session
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(docs_url='/api/docs', openapi_url='/api/openapi.json')


@app.post('/tasks/', response_model=schemas.Task)
async def create_user(
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(get_async_session),
) -> schemas.Task:
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task


@app.get('/tasks/', response_model=list[schemas.Task])
async def read_users(
    db: AsyncSession = Depends(get_async_session),
) -> list[schemas.Task]:
    result = await db.execute(models.Task)
    return result.scalars().all()


if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
