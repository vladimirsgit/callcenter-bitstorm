from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import os
import json

from app.core.constants import OPENAI_GPT_ENDPOINT, OPENAI_GPT_API_KEY
from app.models.chatgpt_response import ChatgptResponse
router = APIRouter()

@router.get("/", response_model=None)
async def chatgpt(prompt: str):

    # Header-ul pentru request
    headers = {
        "Content-Type": "application/json",
        "api-key": OPENAI_GPT_API_KEY,
    }

    # Datele pentru request
    data = {
        "messages": [
            {"role": "system", "content": "Tu esti un asistent AI."},
            {"role": "user", "content": prompt}
        ]
    }

    # Trimitere request
    print("Sending request")
    response = requests.post(OPENAI_GPT_ENDPOINT, headers=headers, json=data)
    print("Request sent")
    rsp = response.json()["choices"][0]["message"]["content"]
    result: ChatgptResponse = ChatgptResponse()
    result.response = rsp
    return result