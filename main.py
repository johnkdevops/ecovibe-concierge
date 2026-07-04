"""
EcoVibe Concierge - FastAPI Service Layer
Imports and mounts the isolated Semantic Orchestrator from modules packaging.
Uses Jinja2 templates to render the frontend view dynamically.
Enriched with SlowAPI IP rate limiting to mitigate Denial-of-Wallet (DoW) attacks.
"""

import os
import sys
import traceback
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# Import SlowAPI rate-limiting modules cleanly
try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded
    limiter_active = True
except ImportError:
    limiter_active = False

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

# Import the modularized Orchestrator class with diagnostic logging
try:
    from modules.orchestrator import AgenticOrchestrator, firestore_active
except Exception as e:
    console.print("[bold red]Import Error:[/bold red] Failed to load modules/orchestrator.py package.")
    console.print(f"[bold red]Exception Details:[/bold red] {e}")
    traceback.print_exc()
    sys.exit(1)

# Initialize FastAPI app
app = FastAPI(title="EcoVibe Concierge Engine")

# Initialize SlowAPI rate limiting core if installed
if limiter_active:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    console.print("[bold green]✓ SlowAPI Rate Limiter Initialized Successfully[/bold green]")
else:
    console.print("[bold yellow]Warning: SlowAPI package not found. Continuing without rate limiting.[/bold yellow]")

# Configure Permissive CORS profiles
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Jinja2 Templates engine with absolute self-healing pathing
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

try:
    templates = Jinja2Templates(directory=TEMPLATES_DIR)
except Exception as e:
    console.print(f"[bold red]Jinja2 Initialization Error:[/bold red] {e}")
    traceback.print_exc()
    sys.exit(1)

# Instantiate the Orchestrator safely
try:
    orchestrator = AgenticOrchestrator()
except Exception as e:
    console.print(f"[bold red]Orchestrator Initialization Error:[/bold red] {e}")
    traceback.print_exc()
    sys.exit(1)

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
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "project_id": GOOGLE_CLOUD_PROJECT,
            "model_name": GEMINI_MODEL
        }
    )

# Apply Rate-Limit decorator conditional check to prevent NameError crashes
if limiter_active:
    @app.post("/chat")
    @limiter.limit("15/minute")
    async def chat(request: Request, payload: ChatMessage):
        if not payload.message.strip():
             raise HTTPException(status_code=400, detail="Input message string cannot be empty.")
        response_text = orchestrator.process(payload.message)
        return {"response": response_text}
else:
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
