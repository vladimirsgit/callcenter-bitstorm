from fastapi import FastAPI, File, UploadFile, APIRouter
from typing import Optional
import os
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI
from app.models.agent import Agent

router = APIRouter()

@router.post("")
async def upload_audio(file: UploadFile):
    pass