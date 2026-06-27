from google import genai

import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from rich.console import Console
from rich.panel import Panel

# Load environment variables
load_dotenv()

# Access variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initializes the client (picks up GEMINI_API_KEY from environment variables)
client = genai.Client(api_key=GEMINI_API_KEY)

print("Available models that support content generation:")
print("-" * 50)

# Iterate through the available models
for model in client.models.list():
    # Filter models by their supported capabilities if needed
    if "generateContent" in model.supported_actions:
        print(f"Model ID: {model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Input Token Limit: {model.input_token_limit}")
        print("-" * 50)