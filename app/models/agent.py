import requests
from app.core.constants import endpoint, api_key

class Agent:
    def __init__(self, prompt: str):
        self.prompt = prompt
        
    def generate_response(self, msg: str):
        # Header-ul pentru request
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key,
        }

        # Datele pentru request
        data = {
            "messages": [
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": msg}
            ]
        }

        # Trimitere request
        print("Sending request")
        response = requests.post(endpoint, headers=headers, json=data)
        print("Request sent")
        rsp = response.json()["choices"][0]["message"]["content"]