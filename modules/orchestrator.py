"""
EcoVibe Concierge - Isolated Semantic Orchestrator Module
Pairs Gemini reasoning models with Cloud Firestore writes and web search grounding.
"""

import os
import sys
import json
from google import genai
from google.genai import types
from rich.console import Console

console = Console()

# ---------------------------------------------------------
# Environment Configurations
# ---------------------------------------------------------
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "eco-vibe-project")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
GEMINI_FALLBACK_MODEL = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-2.5-flash")

# Initialize GenAI Client
try:
    client = genai.Client()
except Exception as e:
    console.print(f"[bold yellow]Warning:[/bold yellow] Could not initialize Client: {e}")
    client = None

# Initialize native Firestore client
firestore_active = False
db_client = None
try:
    from google.cloud import firestore
    db_client = firestore.Client(project=GOOGLE_CLOUD_PROJECT)
    firestore_active = True
    console.print(f"[bold green]✓ Firestore Engine Connected:[/bold green] Active on Project '{GOOGLE_CLOUD_PROJECT}'")
except Exception as e:
    console.print(
        f"[bold yellow]Warning:[/bold yellow] Local Google credentials not found or firestore package missing: {e}\n"
        "[dim yellow]Using high-availability mock fallback for database calculations.[/dim yellow]"
    )


class AgenticOrchestrator:
    """
    An Advanced Semantic Orchestrator that pairs Gemini model reasoning 
    with modular toolsets and database integration.
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
            console.print(f"[yellow]Warning: Primary failed ({primary_error}). Switching to: {GEMINI_FALLBACK_MODEL}...[/yellow]")
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
            - TRACK_EMISSIONS: Log data, calculating distance, fuel metrics, or food intake to write into database trackers.
            - RESEARCH: Queries for grounding facts, environmental documentation parameters, or statistics.
            - GENERAL: Friendly greetings, small talk, or general platform help.

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
            console.print(f"[cyan]Selected Trajectory:[/cyan] {category}")
            
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
        Extracts activity details, performs emission calculation, 
        and writes the entry to Cloud Firestore 'footprints' collection.
        """
        sys_instruction = (
            "You are the specialized EcoVibe Parameter Extractor. Analyze the user statement and "
            "extract the structured transaction properties. "
            "Calculate the emissions_kg based on the standard factors: "
            "- driving: 0.411 kg CO2e per mile"
            "- flight: 0.240 kg CO2e per mile"
            "- meat/beef: 27.0 kg CO2e per kg"
            "Respond strictly in JSON format."
        )

        extraction_prompt = f"""
        Extract attributes from this text.
        Text: "{user_input}"

        Respond with a valid JSON matching this schema:
        {{
            "category": "driving" | "flight" | "diet" | "other",
            "amount": float,
            "unit": "miles" | "km" | "kg" | "hours",
            "emissions_kg": float
        }}
        """

        try:
            config = types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.1,
                system_instruction=sys_instruction
            )
            response = self._generate_with_fallback(contents=extraction_prompt, config=config)
            data = json.loads(response.text.strip())

            # Perform DB Write to Firestore
            doc_id = "mock_sandbox_document"
            db_status_message = ""
            
            if firestore_active and db_client:
                try:
                    doc_ref = db_client.collection("footprints").document()
                    record = {
                        "category": data.get("category", "other"),
                        "amount": data.get("amount", 0.0),
                        "unit": data.get("unit", "miles"),
                        "emissions_kg": data.get("emissions_kg", 0.0),
                        "timestamp": firestore.SERVER_TIMESTAMP
                    }
                    doc_ref.set(record)
                    doc_id = doc_ref.id
                    db_status_message = f"✓ Document `{doc_id}` written successfully to collection `footprints` on project `{GOOGLE_CLOUD_PROJECT}`."
                    console.print(f"[bold green]Firestore Log Success:[/bold green] Added document {doc_id} to collection 'footprints'")
                except Exception as write_error:
                    db_status_message = f"⚠️ Firestore Write Failure: {write_error}"
                    console.print(f"[bold red]Firestore Write Error:[/bold red] {write_error}")
            else:
                db_status_message = "⚡ Sandbox Offline Mode: Calculated metrics parsed successfully (Firestore Client initialized in mock/fallback context)."

            # Formulate friendly synthesis response
            synthesis_prompt = f"""
            Synthesize a brief, encouraging confirmation for the user based on this operation result.
            Operation Status: {db_status_message}
            Calculated Properties:
            - Category: {data.get('category')}
            - Quantity: {data.get('amount')} {data.get('unit')}
            - Footprint: {data.get('emissions_kg')} kg CO2e

            Offer a helpful eco-tip to offset or reduce this activity's impact. Keep under 100 words.
            """

            synthesis_response = self._generate_with_fallback(
                contents=synthesis_prompt,
                config=types.GenerateContentConfig(temperature=0.4)
            )

            return f"### 🚗 Tracker Agent (Firebase Core)\n\n{synthesis_response.text}\n\n**System Logs:**\n`{db_status_message}`"

        except Exception as e:
            return f"### 🚗 Tracker Agent (Error)\nFailed to parse emissions tracking variables: {str(e)}"

    def _handle_mcp_research(self, user_input: str) -> str:
        """
        Researcher specialist channel. Utilizes external public grounding 
        to ensure data points are science-backed.
        """
        sys_instruction = (
            "You are the EcoVibe Researcher Agent. Synthesize verified data points based on official "
            "sustainability parameters. Always provide estimated comparative metrics to support your claims."
        )
        
        config = types.GenerateContentConfig(
            temperature=0.3,
            system_instruction=sys_instruction,
            tools=[{"google_search": {}}]
        )
        
        response = self._generate_with_fallback(contents=user_input, config=config)
        return f"### 🔍 Researcher Agent (Knowledge Base)\n{response.text}"

    def _handle_general(self, user_input: str) -> str:
        chat_prompt = f"You are EcoVibe Concierge, an energetic sustainability platform assistant. Be brief, friendly, and engaging. Respond to: {user_input}"
        response = self._generate_with_fallback(contents=chat_prompt)
        return response.text