import requests
from app.core.constants import OPENAI_GPT_ENDPOINT, OPENAI_GPT_API_KEY
from openai import AzureOpenAI

class Agent:
    def __init__(self, prompt: str):
        self.prompt = prompt
        self.client = AzureOpenAI(
          azure_endpoint = OPENAI_GPT_ENDPOINT, # insert the provided endpoint here 
          api_key=OPENAI_GPT_API_KEY, # insert the provided api key here  
          api_version="2024-08-01-preview"
        )


    def generate_response(self, msg: str):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": msg}
            ]
        )
        return response.to_dict()['choices'][0]['message']['content']