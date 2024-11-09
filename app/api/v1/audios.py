from fastapi import FastAPI, File, UploadFile, APIRouter
from typing import Optional
import os
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI

router = APIRouter()

@router.post("/")
async def upload_audio(file: UploadFile = File(...)):
    
    file_location = f"{os.getcwd()}/app/uploaded_audio/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
        
            
    client = AzureOpenAI(
        api_key=OPENAI_WHISPER_API_KEY, # insert the provided api key here
        api_version="2024-02-01",
        azure_endpoint = OPENAI_WHISPER_ENDPOINT # insert the provided endpoint here
    )

    deployment_id = "whisper"

    result = client.audio.transcriptions.create(
        file=open(file_location, "rb"),            
        model=deployment_id,
        language="ro"
    )

      
    return {"transcription": result}

