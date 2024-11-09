from fastapi import FastAPI, File, UploadFile, APIRouter
from typing import Optional
import os
router = APIRouter()

@router.post("/")
async def upload_audio(file: UploadFile = File(...)):
    
    file_location = f"{os.getcwd()}/app/uploaded_audio/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "message": "Audio file uploaded successfully"}

