from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
import requests
import os
import json

from app.core.constants import endpoint, api_key
from app.models.chatgpt_response import ChatgptResponse
router = APIRouter()

@router.get("/", response_model=None)
async def chatgpt(prompt: str):

    # Header-ul pentru request
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key,
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
    response = requests.post(endpoint, headers=headers, json=data)
    print("Request sent")
    rsp = response.json()["choices"][0]["message"]["content"]
    result: ChatgptResponse = ChatgptResponse()
    result.response = rsp
    return result