from fastapi import FastAPI, File, UploadFile, APIRouter
from typing import Optional
import os
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI

from app.models.agent import Agent

router = APIRouter()

@router.post("")
async def upload_audio(file: UploadFile = File(...)):
    file_location = f"{os.getcwd()}/app/uploaded_audio/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
        
            
    client = AzureOpenAI(
        api_key=OPENAI_WHISPER_API_KEY, # insert the provided api key here
        api_version="2024-10-21",
        azure_endpoint = OPENAI_WHISPER_ENDPOINT # insert the provided endpoint here
    )

    deployment_id = "whisper"

    result = client.audio.transcriptions.create(
        file=open(file_location, "rb"),            
        model=deployment_id,
        language="en"
    )
    potential_problems = [
        "credit_for_personal_needs",
        "deposits",
        "credit_cards",
        "internet_banking",
        "mobile_banking",
        "loans",
        "saving_accounts",
        "other",
    ]
    prompt = f"Please clasify the type of problem the customer is facing. You can only choose between the following options: {", ".join(potential_problems)}. ONE WORDS ANSWER."
    
    
    problem_classification_agent: Agent = Agent(prompt)

    problem_text = problem_classification_agent.generate_response(result.text)
    print(prompt, result.text)
      
    return {"transcription": result, "problem": problem_text}

