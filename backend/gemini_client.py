from dotenv import load_dotenv
load_dotenv()
import os
import requests

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")  # Set your key in environment
GEMINI_EMBEDDING_URL = "https://generativelanguage.googleapis.com/v1beta/models/embedding-001:embedContent?key=" + GEMINI_API_KEY

def get_gemini_embedding(text):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "models/embedding-001",
        "content": {"parts": [{"text": text}]}
    }
    response = requests.post(GEMINI_EMBEDDING_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        # The structure may vary; adjust as needed
        return result["embedding"]["values"]
    else:
        raise Exception(f"Gemini API error: {response.status_code} {response.text}") 