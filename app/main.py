from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.db import init_db, get_session

from app.crud.crud_item import create_item
from app.crud.crud_item import get_items

from app.models.item import Item

from app.api.v1 import items
from app.api.v1 import chatgpt
from app.api.v1 import audios
from app.api.v1 import convos

async def lifespan(app: FastAPI):
    # Startup actions
    await init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(items.router, prefix='/items')
app.include_router(chatgpt.router, prefix='/chatgpt')
app.include_router(audios.router, prefix='/upload-audio')
app.include_router(convos.router, prefix='/convos')

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred. Please try again."},
    )