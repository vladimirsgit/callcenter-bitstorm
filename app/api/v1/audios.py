from fastapi import FastAPI, File, UploadFile, APIRouter, Depends
from typing import Optional
import os
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import OPENAI_WHISPER_API_KEY, OPENAI_WHISPER_ENDPOINT
from openai import AzureOpenAI
from app.models.agent import Agent
from app.models.conversation import Conversation
from app.crud.crud_convos import add_convo
from app.core.db import get_session

router = APIRouter()

async def speech_to_text(file: UploadFile):
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

    whisper_res = client.audio.transcriptions.create(
        file=open(file_location, "rb"),            
        model=deployment_id,
        language="ro"
    )
    print('Whisper called successfully')
    return whisper_res.text

def split_sentiment_summary_suggestion(gpt_response):
    # Extract suggestion
    suggestion = gpt_response.split('suggestions_start:')[-1].strip()
    gpt_response = gpt_response.split('suggestions_start:')[0].strip()
    # Extract summary
    summary = gpt_response.split('summary_start:')[-1].strip()
    gpt_response = gpt_response.split('summary_start:')[0].strip()
    # Extract sentiment score
    sentiment_score = gpt_response.split('sentiment_start:')[-1].strip()

    return sentiment_score, summary, suggestion

@router.post("/final-conv")
async def upload_final_conv(file: UploadFile, db_session: AsyncSession = Depends(get_session)):
    whisper_res = await speech_to_text(file)
    
    prompt = "Please give the conversation a sentiment score from -1.00 to 1.00, using 2 decimals. Also, make a summary of the conversation, and then, add sugggestions so the human agent can learn. Before sentiment write 'sentiment_start:', before summary write: 'summary_start:', and before suggestions add 'suggestions_start:'. Please make sure you use this exact order. Sentiment, summary, suggestions. Thanks!"
    sentiment_analysis_agent: Agent = Agent(prompt)
    
    sentiment_summary_suggestion = sentiment_analysis_agent.generate_response(whisper_res)    
    print('Sentiment summary suggestion generated.')
    
    sentiment_score, summary, suggestion = split_sentiment_summary_suggestion(sentiment_summary_suggestion)
    
    conv: Conversation = Conversation(summary=summary, avg_sentiment=sentiment_score, ai_suggestions=suggestion)
    return await add_convo(db_session, conv)
    
@router.post("")
async def upload_initial_audio_query(file: UploadFile):
    whisper_res = await speech_to_text(file)
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
    
    problem = problem_classification_agent.generate_response(whisper_res)
    sentiment_and_suggestion = sentiment_analysis_agent.generate_response(whisper_res)
    print('Sentiment and problem classif agents called successfully')
    
    file_location = get_fil_loc_based_on_problem(problem)

    suggested_reading = ''
    if file_location:
        file = open(file_location, "r")
        suggested_reading = file.read()
        file.close()
    
    return {"problem": problem, "suggested_reading": suggested_reading, "sentiment_and_suggestion": sentiment_and_suggestion}


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