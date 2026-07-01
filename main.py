"""
EcoVibe Concierge - FastAPI Service Layer
Imports and mounts the isolated Semantic Orchestrator.
Uses Jinja2 templates to render the frontend view dynamically.
"""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# Load environment configurations
load_dotenv()
console = Console()

GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "eco-vibe-project")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IP_ADDRESS = os.getenv("IP_ADDRESS", "0.0.0.0")

try:
    PORT = int(os.getenv("PORT", "8080"))
except ValueError:
    console.print("[bold red]Error:[/bold red] PORT environment variable must be an integer.")
    sys.exit(1)

# Import the isolated Orchestrator class
try:
    from modules.orchestrator import AgenticOrchestrator, firestore_active
except ImportError:
    console.print("[bold red]Import Error:[/bold red] Could not load orchestrator.py module.")
# Initialize FastAPI & Jinja2 Templates engine with absolute self-healing pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
app = FastAPI(title="EcoVibe Concierge Engine")
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Configure Permissive CORS profiles
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate the Orchestrator
orchestrator = AgenticOrchestrator()

# Log operational configuration to console on start
console.print(Panel.fit(
    f"[cyan]Project ID:[/cyan] {GOOGLE_CLOUD_PROJECT}\n"
    f"[cyan]Firestore Engine:[/cyan] {'CONNECTED' if firestore_active else 'OFFLINE/MOCK_FALLBACK'}\n"
    f"[cyan]Jinja2 Template Dir:[/cyan] {TEMPLATES_DIR}\n"
    f"[cyan]Hosting Layer:[/cyan] http://localhost:{PORT}",
    title="[bold green]🌱 EcoVibe Modular Engine Initialized[/bold green]"
))

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # Explicit keyword arguments guarantee compatibility across Starlette 0.28+ and 1.0.0+ signatures
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "project_id": GOOGLE_CLOUD_PROJECT,
            "model_name": GEMINI_MODEL
        }
    )

@app.post("/chat")
async def chat(payload: ChatMessage):
    if not payload.message.strip():
         raise HTTPException(status_code=400, detail="Input message string cannot be empty.")
    response_text = orchestrator.process(payload.message)
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    import os
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(f"{module_name}:app", host=IP_ADDRESS, port=PORT, reload=True)