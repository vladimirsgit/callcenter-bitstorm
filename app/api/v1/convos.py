from fastapi import FastAPI, File, UploadFile, APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import init_db, get_session

import os
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI
from app.models.agent import Agent
from app.models.conversation import Conversation

from app.crud.crud_convos import read_convos, add_convo

router = APIRouter()

@router.post("")
async def get_convos(db_session: AsyncSession = Depends(get_session)):
    return await read_convos(db_session)

@router.post("/create", response_model=Conversation)
async def add_item(conversation: Conversation, db_session: AsyncSession = Depends(get_session)):
    return await add_convo(db_session, conversation)

