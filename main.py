"""
EcoVibe Concierge - Upgraded Main Entry Point
Multi-Agent Sustainability Assistant utilizing the google-genai SDK
Suitable for local run with 'uv' and container deployment on Google Cloud Run.
Includes a automatic fallback strategy from Gemini 3.5 Flash to Gemini 2.5 Flash.
Features an interactive premium Chat UI on the root gateway.
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

# Initialize Rich Console for elegant logging
console = Console()

# ---------------------------------------------------------
# 1. Environment Configurations & Robust Checks
# ---------------------------------------------------------
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "eco-vibe-project")

# Preferred primary and fallback models
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IP_ADDRESS = os.getenv("IP_ADDRESS", "0.0.0.0")

# Cloud Run injects the PORT environment variable dynamically. It must run on 0.0.0.0.
try:
    PORT = int(os.getenv("PORT", "8080"))
except ValueError:
    console.print("[bold red]Error:[/bold red] PORT environment variable must be an integer.")
    sys.exit(1)

# Ensure Google Gen AI SDK is installed
try:
    from google import genai
    from google.genai import types
except ImportError:
    console.print(
        "[bold red]Dependency Error:[/bold red] The official 'google-genai' SDK is missing.\n"
        "Please run: [yellow]uv add google-genai[/yellow] or [yellow]pip install google-genai[/yellow]"
    )
    sys.exit(1)

# Initialize Gemini Client
# It automatically picks up GEMINI_API_KEY from environment variables
try:
    client = genai.Client()
except Exception as e:
    console.print(f"[bold yellow]Warning:[/bold yellow] Could not initialize Google Gen AI Client: {e}")
    console.print("[dim]Ensure your GEMINI_API_KEY or GOOGLE_APPLICATION_CREDENTIALS are set.[/dim]")
    client = None

# ---------------------------------------------------------
# 2. Importing Project Custom Modules
# ---------------------------------------------------------
try:
    from tools.emission_calculator import EmissionCalculator
except ImportError:
    # Fallback mock for self-containment if directory setup differs
    class EmissionCalculator:
        def calculate_emissions(self, activity, value, unit="miles"):
            rate = 0.404 if activity == "driving" else 27.0
            return {"emissions_kg": round(value * rate, 2), "source": "Fallback Mock"}
        def get_recommendations(self, activity, value, unit="miles"):
            return [{"action": "Optimize transit habits", "potential_savings_kg": round(value * 0.2, 1), "difficulty": "easy"}]
        def get_weekly_summary(self, activities):
            return {"total_emissions_kg": 0.0, "status": "Good"}

try:
    from memory.memory_manager import MemoryManager
except ImportError:
    # Fallback mock for self-containment if directory setup differs
    class MemoryManager:
        def __init__(self):
            self.store = {}
        def update_stat(self, key, value):
            self.store[key] = value
        def get_stat(self, key, default=None):
            return self.store.get(key, default)

# Initialize tools and states
calculator = EmissionCalculator()
memory = MemoryManager()

# Log operational variables to the console
console.print(Panel.fit(
    f"[cyan]Project ID:[/cyan] {GOOGLE_CLOUD_PROJECT}\n"
    f"[cyan]Primary Model:[/cyan] {GEMINI_MODEL}\n"
    f"[cyan]Fallback Model:[/cyan] {GEMINI_FALLBACK_MODEL}\n"
    f"[cyan]Hosting Interface:[/cyan] {IP_ADDRESS}:{PORT}\n"
    f"[cyan]Environment Stage:[/cyan] {ENVIRONMENT}",
    title="[bold green]🌱 EcoVibe Engine Config[/bold green]"
))

# ---------------------------------------------------------
# 3. Agentic Semantic Orchestrator
# ---------------------------------------------------------
class AgenticOrchestrator:
    """
    An Agentic Orchestrator that replaces basic string regex search 
    with a structured semantic classification and parameter extraction 
    using Google Gemini models, fully utilizing our custom EmissionCalculator.
    
    Includes built-in dynamic fallback mechanism if the primary Gemini 3.5 model is
    unavailable or fails during generation.
    """
    def __init__(self):
        self.client = client
        self.calculator = calculator
        self.memory = memory

    def _generate_with_fallback(self, contents: str, config: types.GenerateContentConfig = None):
        """
        Attempts generation using the primary GEMINI_MODEL, falling back to
        GEMINI_FALLBACK_MODEL if an unexpected error or quota issue occurs.
        """
        if not self.client:
            raise RuntimeError("Gemini Client is not initialized.")
            
        try:
            # Try primary model first (Gemini 3.5 Flash)
            console.print(f"[dim]Dispatching request to primary model: {GEMINI_MODEL}[/dim]")
            return self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=contents,
                config=config
            )
        except Exception as primary_error:
            console.print(
                f"[yellow]Warning: Primary model ({GEMINI_MODEL}) generation failed. [/yellow]\n"
                f"[dim]Error: {primary_error}[/dim]\n"
                f"[cyan]Retrying execution using fallback model: {GEMINI_FALLBACK_MODEL}...[/cyan]"
            )
            # Try fallback model (Gemini 2.5 Flash)
            return self.client.models.generate_content(
                model=GEMINI_FALLBACK_MODEL,
                contents=contents,
                config=config
            )

    def process(self, user_input: str) -> str:
        console.print("[bold green]Orchestrator [Agent System]:[/bold green] Analyzing request context...")
        
        # If SDK is missing or API key is not configured, fall back gracefully to rule-based routing
        if not self.client:
            console.print("[yellow]Running in Fallback Rule-Based Routing due to missing Gemini configuration...[/yellow]")
            return self._fallback_rule_based_process(user_input)
            
        try:
            # Ask Gemini to classify user intent, detect the calculator category, and extract attributes.
            routing_prompt = f"""
            Analyze the following sustainability user query and classify it into one of these categories matching our calculator's supported activities:
            - TRACK_EMISSIONS: User wants to track a carbon-emitting activity (driving, flying, eating beef, electricity/kWh, bus/train commuting).
            - RESEARCH: User requests facts, alternatives, climate information, guidelines, or statistics.
            - GENERAL: Greet, friendly conversation, or general chit-chat.

            If classifying as TRACK_EMISSIONS, map the request to one of our calculator's target keys:
            - activity_type: Must be exactly one of: 'driving', 'flying', 'beef', 'electricity', or 'public_transport'.
            - value: The numerical quantity/distance of the activity (e.g., 45, 100, 1.2). Return as float or null if not explicitly stated.
            - unit: The unit of measurement (e.g., 'miles', 'km', 'kg', 'meal', 'kwh'). If not specified, choose the logical unit for that activity type.

            Return your response STRICTLY as a valid JSON object matching this schema:
            {{
                "category": "TRACK_EMISSIONS" | "RESEARCH" | "GENERAL",
                "activity_type": "driving" | "flying" | "beef" | "electricity" | "public_transport" | null,
                "value": float | null,
                "unit": string | null
            }}

            User Query: "{user_input}"
            """
            
            # Using custom content fallback logic
            response = self._generate_with_fallback(
                contents=routing_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            
            # Parse structured decision from model response
            decision = json.loads(response.text.strip())
            category = decision.get("category", "GENERAL")
            
            console.print(f"[green]Decision Engine Category:[/green] [bold yellow]{category}[/bold yellow]")
            
            if category == "TRACK_EMISSIONS" and decision.get("activity_type"):
                activity = decision.get("activity_type")
                val = decision.get("value")
                unit = decision.get("unit")
                
                # Assign logical defaults if some elements were omitted by the user
                if not val:
                    defaults = {
                        "driving": (50.0, "miles"),
                        "flying": (1000.0, "miles"),
                        "beef": (1.0, "meal"),
                        "electricity": (150.0, "kwh"),
                        "public_transport": (15.0, "miles")
                    }
                    val, default_unit = defaults.get(activity, (1.0, "unit"))
                    if not unit:
                        unit = default_unit
                elif not unit:
                    unit_defaults = {
                        "driving": "miles",
                        "flying": "miles",
                        "beef": "meal",
                        "electricity": "kwh",
                        "public_transport": "miles"
                    }
                    unit = unit_defaults.get(activity, "unit")

                return self._handle_calculation(activity, val, unit)
                
            elif category == "RESEARCH":
                return self._handle_research(user_input)
                
            else:
                return self._general_response(user_input)

        except Exception as e:
            console.print(f"[bold red]Exception during LLM routing stage:[/bold red] {e}")
            return self._fallback_rule_based_process(user_input)

    def _handle_calculation(self, activity: str, value: float, unit: str) -> str:
        """
        Unified handler that queries the custom EmissionCalculator, saves preferences 
        to MemoryManager, and builds an intuitive markdown analysis.
        """
        # Execute the calculation with our updated custom tool
        result = self.calculator.calculate_emissions(activity, value, unit)
        recs = self.calculator.get_recommendations(activity, value, unit)
        
        # Save structured preference states to context memory
        self.memory.update_stat(f"last_{activity}_emissions", result.get("emissions_kg", 0))
        self.memory.update_stat(f"last_{activity}_value", value)
        self.memory.update_stat(f"last_{activity}_unit", unit)
        
        # Set visual design decorations
        icons = {
            "driving": "🚗",
            "flying": "✈️",
            "beef": "🥩",
            "electricity": "⚡",
            "public_transport": "🚌"
        }
        icon = icons.get(activity, "🌱")
        activity_title = activity.replace("_", " ").title()
        
        response = f"### {icon} Tracker Agent: Emission Calculation ({activity_title})\n"
        
        if "error" in result:
            response += f"⚠️ **Calculation Error:** {result['error']}\n"
            return response
            
        response += f"Based on your input of **{value} {unit}**, you emitted roughly **{result.get('emissions_kg', 0.0)} kg CO₂e**.\n\n"
        response += f"*Source: {result.get('source', 'Emission Calculator tool')}*\n\n"
        
        if recs:
            response += "#### 🌿 Tailored Action Recommendations:\n"
            for r in recs:
                difficulty_badge = f"`[{r.get('difficulty', 'medium').upper()}]`"
                response += f"• **{r['action']}** — can help reduce emissions by ~**{r['potential_savings_kg']} kg** {difficulty_badge}\n"
        else:
            response += "💡 *EcoVibe Tip:* Shift away from heavy carbon options to clean alternatives to optimize your footprint today!"
            
        return response

    def _handle_research(self, user_input: str) -> str:
        if not self.client:
            return "### 🔍 Researcher Agent:\nSwitching to alternative commutes or diet patterns dramatically reduces climate impact. Connect your API key to research real-time facts."

        # Leverage Gemini for grounded research synthesis with dynamic model fallback
        research_prompt = f"""
        You are the specialist Researcher Agent in EcoVibe Concierge.
        Provide a concise, science-backed sustainability advice/analysis on the following subject:
        "{user_input}"
        Provide facts, references, or alternative methods to reduce impact. Keep your response under 100 words.
        """
        try:
            response = self._generate_with_fallback(contents=research_prompt)
            return f"### 🔍 Researcher Agent: Grounded Facts\n{response.text}"
        except Exception as e:
            return f"### 🔍 Researcher Agent: Error\nCould not perform sustainability research due to service error: {e}"

    def _general_response(self, user_input: str) -> str:
        if not self.client:
            return "Hello! I am EcoVibe Concierge. Tell me about your commutes, flights, utilities, diet, or ask for research."
            
        chat_prompt = f"""
        You are EcoVibe Concierge, a helpful, conversational, and energetic personal sustainability assistant.
        Reply friendly, welcome the user, and offer to track utility bills, flight trips, car travel, diets, or explore ecological alternatives.
        User message: "{user_input}"
        """
        try:
            response = self._generate_with_fallback(contents=chat_prompt)
            return response.text
        except Exception as e:
            return f"Hello! Welcome to EcoVibe Concierge. (An issue occurred retrieving LLM response: {e})"

    def _fallback_rule_based_process(self, user_input: str) -> str:
        """
        Graceful local fallback matching mechanism if the Gemini API cannot be reached.
        """
        import re
        input_lower = user_input.lower()
        
        if any(word in input_lower for word in ["drove", "drive", "driving", "miles", "km", "car"]):
            numbers = re.findall(r'\d+', user_input)
            distance = int(numbers[0]) if numbers else 50
            return self._handle_calculation("driving", distance, "miles")
            
        elif any(word in input_lower for word in ["eat", "ate", "lunch", "dinner", "meal", "beef", "food"]):
            numbers = re.findall(r'\d+', user_input)
            val = float(numbers[0]) if numbers else 1.0
            return self._handle_calculation("beef", val, "meal")
            
        elif any(word in input_lower for word in ["fly", "flight", "flying", "plane"]):
            numbers = re.findall(r'\d+', user_input)
            val = float(numbers[0]) if numbers else 1000.0
            return self._handle_calculation("flying", val, "miles")
            
        elif any(word in input_lower for word in ["electricity", "kwh", "power", "utility"]):
            numbers = re.findall(r'\d+', user_input)
            val = float(numbers[0]) if numbers else 150.0
            return self._handle_calculation("electricity", val, "kwh")
            
        elif any(word in input_lower for word in ["bus", "train", "transit", "subway"]):
            numbers = re.findall(r'\d+', user_input)
            val = float(numbers[0]) if numbers else 15.0
            return self._handle_calculation("public_transport", val, "miles")
            
        else:
            return "### 🌱 EcoVibe Concierge (Local Fallback Mode)\nI'm ready to keep track of your carbon footprint. Try telling me about your car trips, flights, electricity bills, bus commutes, or beef consumption!"


# Initialize our improved orchestrator
orchestrator = AgenticOrchestrator()

# ---------------------------------------------------------
# 4. FastAPI Setup
# ---------------------------------------------------------
app = FastAPI(
    title="EcoVibe Concierge",
    description="Multi-Agent Sustainability Assistant with Real-Time Routing and Model Fallback"
)

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>EcoVibe Concierge — AI Sandbox</title>
        <!-- Tailwind CSS -->
        <script src="https://cdn.tailwindcss.com"></script>
        <!-- Marked.js for markdown rendering -->
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Inter', sans-serif;
            }}
            /* Custom markdown styling inside messages */
            .prose-custom h3 {{
                font-size: 1.125rem;
                font-weight: 700;
                color: #065f46;
                margin-top: 0.5rem;
                margin-bottom: 0.25rem;
            }}
            .prose-custom h4 {{
                font-size: 1rem;
                font-weight: 600;
                color: #047857;
                margin-top: 0.5rem;
                margin-bottom: 0.25rem;
            }}
            .prose-custom ul {{
                list-style-type: disc;
                padding-left: 1.25rem;
                margin-bottom: 0.5rem;
            }}
            .prose-custom li {{
                margin-bottom: 0.25rem;
            }}
            .prose-custom code {{
                background-color: #ecfdf5;
                color: #065f46;
                padding: 0.125rem 0.25rem;
                border-radius: 0.25rem;
                font-family: monospace;
                font-size: 0.875rem;
            }}
            /* Scrollbar styling */
            ::-webkit-scrollbar {{
                width: 6px;
            }}
            ::-webkit-scrollbar-track {{
                background: transparent;
            }}
            ::-webkit-scrollbar-thumb {{
                background: #cbd5e1;
                border-radius: 4px;
            }}
            ::-webkit-scrollbar-thumb:hover {{
                background: #94a3b8;
            }}
        </style>
    </head>
    <body class="bg-slate-50 text-slate-800 h-screen flex flex-col overflow-hidden">
        
        <!-- Header -->
        <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between shrink-0">
            <div class="flex items-center gap-3">
                <span class="text-3xl">🌱</span>
                <div>
                    <h1 class="text-lg font-bold text-emerald-800 tracking-tight leading-none">EcoVibe Concierge</h1>
                    <span class="text-xs text-slate-500">Multi-Agent Sustainability Engine</span>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    Online (Port {PORT})
                </span>
            </div>
        </header>

        <!-- Main Workspace -->
        <main class="flex-1 flex overflow-hidden">
            
            <!-- Left Sidebar - System Diagnostics -->
            <div class="w-80 border-r border-slate-200 bg-white p-6 flex flex-col justify-between shrink-0 hidden md:flex">
                <div class="space-y-6">
                    <div>
                        <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Orchestration Models</h2>
                        <div class="space-y-2.5">
                            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                                <span class="text-[10px] uppercase font-bold text-emerald-600 block mb-0.5">Primary Target</span>
                                <code class="text-xs font-medium text-slate-700">{GEMINI_MODEL}</code>
                            </div>
                            <div class="p-3 bg-slate-50 rounded-lg border border-slate-200">
                                <span class="text-[10px] uppercase font-bold text-cyan-600 block mb-0.5">Fallback Target</span>
                                <code class="text-xs font-medium text-slate-700">{GEMINI_FALLBACK_MODEL}</code>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Active Pipeline</h2>
                        <ul class="space-y-2 text-xs font-medium text-slate-600">
                            <li class="flex items-center gap-2 text-emerald-700">
                                <span class="text-sm">🤖</span> orchestrator/SKILL.md
                            </li>
                            <li class="flex items-center gap-2">
                                <span class="text-sm">🚗</span> skills/tracker-skill
                            </li>
                            <li class="flex items-center gap-2">
                                <span class="text-sm">🔍</span> skills/researcher-skill
                            </li>
                            <li class="flex items-center gap-2">
                                <span class="text-sm">📅</span> skills/planner-skill
                            </li>
                        </ul>
                    </div>

                    <div>
                        <h2 class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Local Project Registry</h2>
                        <div class="space-y-1.5 text-xs text-slate-500 font-mono bg-slate-50 p-3 rounded-lg border border-slate-200">
                            <div>PROJECT_ID: {GOOGLE_CLOUD_PROJECT}</div>
                            <div>STAGE: {ENVIRONMENT}</div>
                            <div>LOC: {IP_ADDRESS}</div>
                        </div>
                    </div>
                </div>

                <div class="text-[10px] text-slate-400 border-t border-slate-100 pt-4">
                    5-Day Agentic Development Lifecycle<br>
                    Capstone Project Portfolio Platform
                </div>
            </div>

            <!-- Right Area - The Main Chat Interface -->
            <div class="flex-1 flex flex-col bg-slate-50">
                <!-- Message Thread Panel -->
                <div id="chat-thread" class="flex-1 overflow-y-auto p-6 space-y-6">
                    <!-- Welcome System message -->
                    <div class="flex gap-4 max-w-3xl">
                        <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-sm shrink-0 shadow-sm border border-emerald-200">
                            🌱
                        </div>
                        <div class="bg-white rounded-2xl px-5 py-4 shadow-sm border border-slate-100 space-y-2">
                            <p class="font-semibold text-emerald-800 text-sm">EcoVibe Concierge Orchestrator</p>
                            <p class="text-sm text-slate-600 leading-relaxed">
                                Welcome to your local test environment! I am ready to coordinate our team of 4 specialized AI agents to track your carbon calculations, goal-setting schedules, and custom ecological research.
                            </p>
                            <p class="text-xs text-slate-400 italic">
                                Try asking a question below or selecting a quick-test prompt chip.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Input Panel -->
                <div class="p-6 bg-white border-t border-slate-200 shrink-0">
                    <!-- Quick-Action Suggestion Chips -->
                    <div class="max-w-3xl mx-auto mb-4 flex flex-wrap gap-2">
                        <button onclick="useChip('I drove 45 miles today in my gasoline car')" class="px-3 py-1.5 bg-slate-50 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-medium text-slate-600 rounded-lg border border-slate-200 hover:border-emerald-200 transition-all duration-150">
                            🚗 I drove 45 miles today
                        </button>
                        <button onclick="useChip('I had lunch containing 0.5 kg of beef')" class="px-3 py-1.5 bg-slate-50 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-medium text-slate-600 rounded-lg border border-slate-200 hover:border-emerald-200 transition-all duration-150">
                            🥩 I had a beef meal
                        </button>
                        <button onclick="useChip('Compare the impact of driving vs. taking a flight')" class="px-3 py-1.5 bg-slate-50 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-medium text-slate-600 rounded-lg border border-slate-200 hover:border-emerald-200 transition-all duration-150">
                            🔍 Compare transit footprints
                        </button>
                        <button onclick="useChip('Research the environmental benefits of electric vehicles')" class="px-3 py-1.5 bg-slate-50 hover:bg-emerald-50 hover:text-emerald-700 text-xs font-medium text-slate-600 rounded-lg border border-slate-200 hover:border-emerald-200 transition-all duration-150">
                            ⚡ Research EV benefits
                        </button>
                    </div>

                    <!-- Input Form block -->
                    <form id="chat-form" onsubmit="submitQuery(event)" class="max-w-3xl mx-auto flex gap-3">
                        <input id="chat-input" type="text" placeholder="Type a message or task for the Orchestrator..." autocomplete="off" class="flex-1 px-4 py-3 border border-slate-200 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 outline-none rounded-xl text-sm transition-all duration-150 bg-slate-50 focus:bg-white">
                        <button type="submit" class="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-5 py-3 rounded-xl text-sm shadow-sm hover:shadow transition-all duration-150 flex items-center justify-center shrink-0">
                            Send Message
                        </button>
                    </form>
                </div>
            </div>

        </main>

        <!-- Javascript Operations Layer -->
        <script>
            const threadEl = document.getElementById('chat-thread');
            const inputEl = document.getElementById('chat-input');

            // Quick function to trigger chip prompt selection
            function useChip(text) {{
                inputEl.value = text;
                inputEl.focus();
            }}

            // Append messages locally to the scroll thread
            function appendMessage(sender, text, isUser) {{
                const wrapper = document.createElement('div');
                wrapper.className = `flex gap-4 max-w-3xl ${{isUser ? 'ml-auto flex-row-reverse' : ''}}`;

                const avatar = document.createElement('div');
                avatar.className = `w-8 h-8 rounded-full flex items-center justify-center text-sm shrink-0 shadow-sm border ${{
                    isUser ? 'bg-slate-200 border-slate-300' : 'bg-emerald-100 border-emerald-200'
                }}`;
                avatar.innerText = isUser ? '🧑' : '🌱';

                const card = document.createElement('div');
                card.className = `rounded-2xl px-5 py-4 shadow-sm border ${{
                    isUser ? 'bg-slate-100 border-slate-200 text-slate-700' : 'bg-white border-slate-100 space-y-2'
                }}`;

                const header = document.createElement('p');
                header.className = `font-semibold text-xs ${{isUser ? 'text-slate-500 text-right' : 'text-emerald-800'}}`;
                header.innerText = isUser ? 'You' : 'EcoVibe Concierge Orchestrator';

                const content = document.createElement('div');
                content.className = `text-sm leading-relaxed ${{isUser ? '' : 'prose-custom'}}`;
                
                // Parse markdown strictly if sent by AI, otherwise text-only
                if (isUser) {{
                    content.innerText = text;
                }} else {{
                    content.innerHTML = marked.parse(text);
                }}

                card.appendChild(header);
                card.appendChild(content);
                wrapper.appendChild(avatar);
                wrapper.appendChild(card);
                threadEl.appendChild(wrapper);

                // Autoscroll to bottom of conversation thread
                threadEl.scrollTop = threadEl.scrollHeight;
            }}

            // Loading indicator display
            function appendLoader() {{
                const loader = document.createElement('div');
                loader.id = 'active-loader';
                loader.className = 'flex gap-4 max-w-3xl';
                loader.innerHTML = `
                    <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-sm shrink-0 border border-emerald-200">🌱</div>
                    <div class="bg-white rounded-2xl px-5 py-4 shadow-sm border border-slate-100 flex items-center gap-1">
                        <span class="h-2 w-2 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                        <span class="h-2 w-2 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                        <span class="h-2 w-2 bg-emerald-500 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
                    </div>
                `;
                threadEl.appendChild(loader);
                threadEl.scrollTop = threadEl.scrollHeight;
            }}

            function removeLoader() {{
                const loader = document.getElementById('active-loader');
                if (loader) loader.remove();
            }}

            // Form Submit asynchronous fetch execution
            async function submitQuery(event) {{
                event.preventDefault();
                const query = inputEl.value.trim();
                if (!query) return;

                // Display user's text on UI instantly
                appendMessage('User', query, true);
                inputEl.value = '';
                appendLoader();

                try {{
                    const response = await fetch('/chat', {{
                        method: 'POST',
                        headers: {{
                            'Content-Type': 'application/json'
                        }},
                        body: JSON.stringify({{ message: query }})
                    }});

                    const data = await response.json();
                    removeLoader();

                    if (response.ok && data.response) {{
                        appendMessage('AI', data.response, false);
                    }} else {{
                        appendMessage('AI', "⚠️ **Local Server Error:** Failed to resolve the orchestrator response. Check your local FastAPI console outputs.", false);
                    }}
                }} catch (err) {{
                    removeLoader();
                    appendMessage('AI', "❌ **Network Connection Refused:** Ensure your FastAPI local server is active, is running on port 8080, and isn't blocked by a local firewall.", false);
                }}
            }}
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat(payload: ChatMessage):
    if not payload.message.strip():
         raise HTTPException(status_code=400, detail="Empty messages are not supported.")
    
    # Process request using agentic model router
    response_text = orchestrator.process(payload.message)
    return {"response": response_text}

# ---------------------------------------------------------
# 5. Server Launcher block
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    
    # Securely bind the hosting parameters
    # Binding on 0.0.0.0 and dynamically reading standard environment PORT is essential for Cloud Run.
    console.print(f"[bold green]✓ Starting service on {IP_ADDRESS}:{PORT}...[/bold green]")
    
    # Dynamically extract module name based on current file execution context
    module_name = os.path.splitext(os.path.basename(__file__))[0]
    uvicorn.run(f"{module_name}:app", host=IP_ADDRESS, port=PORT, reload=True)