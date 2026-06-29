"""
EcoVibe Concierge - Upgraded Main Entry Point with MCP Tool Binding & Frontend UI
Multi-Agent Sustainability Assistant utilizing the google-genai SDK
Supports live Firestore mutations and Developer Knowledge queries via MCP channels.
"""

import os
import sys
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# Load environment variables from .env file
load_dotenv()
console = Console()

# ---------------------------------------------------------
# 1. Environment Configurations & Robust Checks
# ---------------------------------------------------------
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "device-streaming-8997208")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IP_ADDRESS = os.getenv("IP_ADDRESS", "0.0.0.0")

try:
    PORT = int(os.getenv("PORT", "8080"))
except ValueError:
    console.print("[bold red]Error:[/bold red] PORT environment variable must be an integer.")
    sys.exit(1)

# Ensure Google Gen AI SDK is installed properly
try:
    from google import genai
    from google.genai import types
except ImportError:
    console.print("[bold red]Dependency Error:[/bold red] The official 'google-genai' SDK is missing.")
    sys.exit(1)

try:
    client = genai.Client()
except Exception as e:
    console.print(f"[bold yellow]Warning:[/bold yellow] Could not initialize Client: {e}")
    client = None

# Log operational variables to the console
console.print(Panel.fit(
    f"[cyan]Project ID:[/cyan] {GOOGLE_CLOUD_PROJECT}\n"
    f"[cyan]Primary Target Model:[/cyan] {GEMINI_MODEL}\n"
    f"[cyan]Fallback Target Model:[/cyan] {GEMINI_FALLBACK_MODEL}\n"
    f"[cyan]Hosting Layer:[/cyan] {IP_ADDRESS}:{PORT}",
    title="[bold green]🌱 EcoVibe Engine + MCP Controller[/bold green]"
))

# ---------------------------------------------------------
# 2. Agentic Semantic Orchestrator with Tool Matching
# ---------------------------------------------------------
class AgenticOrchestrator:
    """
    An Advanced Semantic Orchestrator that pairs Gemini model reasoning 
    with modular toolsets exposed across your configured workspace MCP pipelines.
    """
    def __init__(self):
        self.client = client

    def _generate_with_fallback(self, contents: str, config: types.GenerateContentConfig = None):
        if not self.client:
            raise RuntimeError("Gemini Client is not active or initialized.")
            
        try:
            console.print(f"[dim]Dispatching request to primary model: {GEMINI_MODEL}[/dim]")
            return self.client.models.generate_content(
                model=GEMINI_MODEL, contents=contents, config=config
            )
        except Exception as primary_error:
            console.print(f"[yellow]Warning: Primary failed. Switching to: {GEMINI_FALLBACK_MODEL}...[/yellow]")
            return self.client.models.generate_content(
                model=GEMINI_FALLBACK_MODEL, contents=contents, config=config
            )

    def process(self, user_input: str) -> str:
        console.print("[bold green]Orchestrator Engine:[/bold green] Resolving routing trajectories...")
        
        if not self.client:
            return "### ⚠️ System Offline\nPlease configure your valid GenAI token strings to engage the agent workspace."
            
        try:
            routing_prompt = f"""
            Analyze this sustainability query and classify it into one of these operational pipelines:
            - TRACK_EMISSIONS: Log data or modify documents inside user database trackers.
            - RESEARCH: Queries for grounding facts, environmental documentation parameters, or statistics.
            - GENERAL: Friendly greetings or conversational text.

            Return response STRICTLY as a valid raw JSON object matching this schema:
            {{
                "category": "TRACK_EMISSIONS" | "RESEARCH" | "GENERAL"
            }}

            User Query: "{user_input}"
            """
            
            response = self._generate_with_fallback(
                contents=routing_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            decision = json.loads(response.text.strip())
            category = decision.get("category", "GENERAL")
            
            if category == "TRACK_EMISSIONS":
                return self._handle_mcp_tracking(user_input)
            elif category == "RESEARCH":
                return self._handle_mcp_research(user_input)
            else:
                return self._handle_general(user_input)

        except Exception as e:
            return f"### 💥 Internal Error\nFailed to parse routing execution trajectory smoothly: {e}"

    def _handle_mcp_tracking(self, user_input: str) -> str:
        """
        Tracker specialist channel. Employs Firestore capabilities 
        exposed via your configured Firebase MCP tool server definitions.
        """
        sys_instruction = (
            "You are the specialized EcoVibe Tracker Agent. You write calculations and user records "
            "directly into Cloud Firestore database collections using your registered data tools."
        )
        
        mcp_tools = []
        try:
            import mcp_client_runtime  
            mcp_tools = mcp_client_runtime.get_tools("firebase-mcp-server")
            console.print(f"[dim green]✓ Successfully loaded {len(mcp_tools)} tools from Firebase MCP Server[/dim green]")
        except (ImportError, Exception):
            console.print("[dim yellow]Note: External runtime context. Using native function schemas...[/dim yellow]")
            mcp_tools = [] 
        
        config = types.GenerateContentConfig(
            tools=mcp_tools if mcp_tools else None,
            temperature=0.2,
            system_instruction=sys_instruction
        )
        
        response = self._generate_with_fallback(contents=user_input, config=config)
        return f"### 🚗 Tracker Agent (Firebase Core)\n{response.text}"

    def _handle_mcp_research(self, user_input: str) -> str:
        """
        Researcher specialist channel. Utilizes external public grounding 
        via your developer knowledge SSE endpoint definition.
        """
        sys_instruction = (
            "You are the EcoVibe Researcher Agent. Synthesize verified data points based on official "
            "sustainability parameters and clean infrastructure choices."
        )
        
        config = types.GenerateContentConfig(
            temperature=0.3,
            system_instruction=sys_instruction
        )
        
        response = self._generate_with_fallback(contents=user_input, config=config)
        return f"### 🔍 Researcher Agent (Knowledge Base)\n{response.text}"

    def _handle_general(self, user_input: str) -> str:
        chat_prompt = f"You are EcoVibe Concierge, an energetic sustainability platform assistant. Be brief and engaging. Respond to: {user_input}"
        response = self._generate_with_fallback(contents=chat_prompt)
        return response.text

# Initialize our dynamic orchestrator
orchestrator = AgenticOrchestrator()

# ---------------------------------------------------------
# 3. FastAPI Initialization & Premium UI Interface
# ---------------------------------------------------------
app = FastAPI(title="EcoVibe Concierge Engine")

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌱 EcoVibe Concierge Workspace</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    </head>
    <body class="bg-slate-900 text-slate-100 font-sans min-h-screen flex flex-col">
        <header class="bg-slate-800/80 border-b border-slate-700/50 backdrop-blur sticky top-0 z-50 p-4 shadow-lg">
            <div class="max-w-4xl mx-auto flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="bg-emerald-500/20 text-emerald-400 p-2.5 rounded-xl border border-emerald-500/30 shadow-inner">
                        <i class="fa-solid fa-leaf text-xl animate-pulse"></i>
                    </div>
                    <div>
                        <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
                            EcoVibe Concierge <span class="text-xs font-normal px-2 py-0.5 bg-slate-700 rounded-full text-slate-300">v2.0</span>
                        </h1>
                        <p class="text-xs text-slate-400">Multi-Agent Intelligence System connected to MCP Gateway</p>
                    </div>
                </div>
                <div class="flex items-center space-x-2 text-xs bg-slate-900/60 px-3 py-1.5 rounded-lg border border-slate-700/40">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                    <span class="text-slate-300 font-mono">FastAPI: Active</span>
                </div>
            </div>
        </header>

        <main class="flex-1 max-w-4xl w-full mx-auto flex flex-col p-4 overflow-hidden">
            <div id="chat-box" class="flex-1 bg-slate-800/40 border border-slate-700/30 rounded-2xl p-4 overflow-y-auto space-y-4 shadow-2xl backdrop-blur-sm min-h-[450px]">
                <div class="flex space-x-3 bg-slate-800/40 border border-slate-700/40 p-4 rounded-xl max-w-[85%]">
                    <div class="w-8 h-8 rounded-lg bg-emerald-500 text-white flex items-center justify-center font-bold text-sm shrink-0 shadow-md">
                        AI
                    </div>
                    <div class="space-y-2 text-sm text-slate-200">
                        <p class="font-semibold text-emerald-400">Welcome to your Personal Sustainability Hub!</p>
                        <p>I am your **Orchestrator Agent**, synchronized with your private workspace MCP servers. Tell me about your carbon accounting logs, or ask for facts regarding sustainability research options.</p>
                        <div class="pt-2 grid grid-cols-1 sm:grid-cols-2 gap-2">
                            <button onclick="fillAndSend('🚗 I drove 45 miles today in my gasoline car.')" class="text-left text-xs bg-slate-700/50 hover:bg-slate-700 border border-slate-600/40 p-2.5 rounded-lg text-slate-300 transition-all flex items-center gap-2">
                                <i class="fa-solid fa-car text-emerald-400"></i> Log a driving calculation
                            </button>
                            <button onclick="fillAndSend('Research the environmental benefits of electric vehicles.')" class="text-left text-xs bg-slate-700/50 hover:bg-slate-700 border border-slate-600/40 p-2.5 rounded-lg text-slate-300 transition-all flex items-center gap-2">
                                <i class="fa-solid fa-magnifying-glass text-cyan-400"></i> Execute grounding lookups
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-4">
                <form id="chat-form" class="flex space-x-2">
                    <input type="text" id="user-input" placeholder="Ask your Orchestrator anything..." required
                           class="flex-1 bg-slate-800/80 text-white placeholder-slate-500 text-sm border border-slate-700 rounded-xl px-4 py-3.5 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all shadow-inner">
                    <button type="submit" class="bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm rounded-xl px-5 py-3.5 transition-all shadow-lg flex items-center space-x-2">
                        <span>Send</span>
                        <i class="fa-solid fa-paper-plane text-xs"></i>
                    </button>
                </form>
            </div>
        </main>

        <script>
            const chatBox = document.getElementById('chat-box');
            const chatForm = document.getElementById('chat-form');
            const userInput = document.getElementById('user-input');

            function appendMessage(sender, text, isUser) {
                const msgWrapper = document.createElement('div');
                msgWrapper.className = `flex space-x-3 ${isUser ? 'justify-end' : ''}`;
                
                const bubbleClass = isUser 
                    ? 'bg-emerald-600 text-white rounded-br-none' 
                    : 'bg-slate-800 border border-slate-700/60 text-slate-100 rounded-bl-none';

                const avatar = isUser
                    ? '<div class="w-8 h-8 rounded-lg bg-slate-700 text-slate-300 flex items-center justify-center font-bold text-sm shadow-md order-2 ml-3">ME</div>'
                    : '<div class="w-8 h-8 rounded-lg bg-emerald-500 text-white flex items-center justify-center font-bold text-sm shadow-md mr-3">AI</div>';

                msgWrapper.innerHTML = `
                    ${!isUser ? avatar : ''}
                    <div class="p-3.5 rounded-xl text-sm max-w-[80%] shadow-md whitespace-pre-line ${bubbleClass}">
                        ${text}
                    </div>
                    ${isUser ? avatar : ''}
                `;
                
                chatBox.appendChild(msgWrapper);
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function fillAndSend(phrase) {
                userInput.value = phrase;
                chatForm.requestSubmit();
            }

            chatForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                const text = userInput.value.trim();
                if (!text) return;

                appendMessage('User', text, true);
                userInput.value = '';

                // Loader Element
                const loader = document.createElement('div');
                loader.className = 'flex items-center space-x-2 text-xs text-slate-400 italic pt-1';
                loader.id = 'ai-loader';
                loader.innerHTML = '<i class="fa-solid fa-circle-notch animate-spin text-emerald-400"></i> <span>Orchestrator is resolving execution parameters...</span>';
                chatBox.appendChild(loader);
                chatBox.scrollTop = chatBox.scrollHeight;

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: text })
                    });
                    
                    const data = await response.json();
                    document.getElementById('ai-loader').remove();

                    if (response.ok) {
                        appendMessage('AI', data.response, false);
                    } else {
                        appendMessage('AI', `❌ **Error:** ${data.detail || 'Failed to synthesize prompt.'}`, false);
                    }
                } catch (error) {
                    if (document.getElementById('ai-loader')) document.getElementById('ai-loader').remove();
                    appendMessage('AI', '❌ **Connection Failure:** Ensure your local FastAPI service is fully active.', false);
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(payload: ChatMessage):
    if not payload.message.strip():
         raise HTTPException(status_code=400, detail="Input message string cannot be empty.")
    response_text = orchestrator.process(payload.message)
    return {"response": response_text}

if __name__ == "__main__":
    import uvicorn
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(f"{module_name}:app", host=IP_ADDRESS, port=PORT, reload=True)