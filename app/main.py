from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import init_db, get_session

from app.crud.crud_item import create_item
from app.crud.crud_item import get_items

from app.models.item import Item

from app.api.v1 import items

async def lifespan(app: FastAPI):
    # Startup actions
    await init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(items.router, prefix='/items')


