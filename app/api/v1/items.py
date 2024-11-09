from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import init_db, get_session

from app.crud.crud_item import create_item
from app.crud.crud_item import get_items

from app.models.item import Item

from app.api.v1 import items
import openai
import os

router = APIRouter()


@router.post("/create", response_model=Item)
async def add_item(item: Item, db_session: AsyncSession = Depends(get_session)):
    return await create_item(db_session, item)

@router.get("/", response_model=list[Item])
async def read_items(db_session: AsyncSession = Depends(get_session)):
    return await get_items(db_session)

