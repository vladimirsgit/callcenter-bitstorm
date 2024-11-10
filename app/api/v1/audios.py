from fastapi import FastAPI, File, UploadFile, APIRouter, JSONResponse
from typing import Optional
import os
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI
from app.models.agent import Agent

router = APIRouter()

@router.post("")
async def upload_audio(file: UploadFile):
    if not file:
        return
    print('Opening file', file.filename)
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
    print('Whisper called successfully')
    potential_problems = [
        "personal_loans",
        "withdrawals",
        "transactions",
        "credit_cards",
        "mobile_banking",
        "saving_accounts",
        'angry',
        "other",
    ]
    prompt = f"Please clasify the type of problem the customer is facing. You can only choose between the following options: {", ".join(potential_problems)}. ONE WORD ANSWER."
    problem_classification_agent: Agent = Agent(prompt)

    prompt = f"Please tell me if the sentiment of this customer is positive, negative or neutral, and give it a score from -1.00 to 1.00, using 2 decimals. Also, add suggestions on how a human agent might handle the situation. First word MUST be the sentiment, then the score, separated by a coma. Then at the end, the suggestions. Thanks!"
    sentiment_analysis_agent: Agent = Agent(prompt)
    
    problem = problem_classification_agent.generate_response(result.text)
    sentiment_and_suggestion = sentiment_analysis_agent.generate_response(result.text)
    print('Sentiment and problem classif agents called successfully')
    
    file_location = get_fil_loc_based_on_problem(problem)

    suggested_reading = ''
    if file_location:
        file = open(file_location, "r")
        suggested_reading = file.read()
        file.close()
    
    headers = {
        "Access-Control-Allow-Origin": "http://localhost:3000",
        "Access-Control-Allow-Credentials": "true",
    }
    return JSONResponse(content = {"problem": problem, "suggested_reading": suggested_reading, "sentiment_and_suggestion": sentiment_and_suggestion}, headers = headers)


def get_fil_loc_based_on_problem(problem):
    root_folder = 'app/utils/bank_website_info/'
    if problem == 'personal_loans':
        return f'{root_folder}credit_for_personal_needs.txt'
    elif problem == 'credit_cards':
        return f'{root_folder}credit_cards.txt'
    elif problem == 'mobile_banking':
        return f'{root_folder}mobile_banking.txt'
    elif problem == 'savings_accounts.txt':
        return f'{root_folder}savings_accounts.txt'
    
    return None