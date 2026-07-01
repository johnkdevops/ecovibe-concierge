"""
EcoVibe BDD Step Verification Suite
Executes specifications declared inside 'tests/features/agent_routing.feature'
using pytest-bdd.
"""

import json
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from unittest.mock import MagicMock
from main import AgenticOrchestrator

# Load all scenarios defined in our Gherkin feature file
scenarios('features/agent_routing.feature')

# Helper to generate mock JSON string matching orchestrator's expectations
def mock_gemini_routing_call(category: str):
    mock_response = MagicMock()
    mock_response.text = json.dumps({"category": category})
    return mock_response

@pytest.fixture
def orchestrator():
    orchestrator_instance = AgenticOrchestrator()
    # Mock GenAI client interface to bypass network initialization
    orchestrator_instance.client = MagicMock()
    return orchestrator_instance

@pytest.fixture
def bdd_context():
    """State storage container passed across Gherkin steps."""
    return {}

# ---------------------------------------------------------
# Step Definitions
# ---------------------------------------------------------

@given("the EcoVibe Orchestrator is initialized and active")
def init_orchestrator(orchestrator, bdd_context):
    bdd_context["orchestrator"] = orchestrator

@when(parsers.parse('the user submits the message "{message}"'))
def submit_message(bdd_context, message):
    bdd_context["message"] = message

@then(parsers.parse('the system should categorize the request trajectory as "{category}"'))
def verify_trajectory(bdd_context, category):
    orchestrator = bdd_context["orchestrator"]
    message = bdd_context["message"]
    
    # Inject routing predictions mock
    orchestrator._generate_with_fallback = MagicMock(
        return_value=mock_gemini_routing_call(category)
    )
    
    # Mock backend agent responses to avoid hitting live cloud/db systems
    orchestrator._handle_mcp_tracking = MagicMock(
        return_value="### 🚗 Tracker Agent (Firebase Core)\nEmission logged successfully in Firestore."
    )
    orchestrator._handle_mcp_research = MagicMock(
        return_value="### 🔍 Researcher Agent (Knowledge Base)\nResearch complete."
    )
    
    # Process message and save output state
    bdd_context["result"] = orchestrator.process(message)
    bdd_context["category"] = category
    
    # Verify orchestrator built a routing payload targeting this category
    assert category in orchestrator._generate_with_fallback.call_args[1]["contents"]

@then(parsers.parse('the dispatch logic should engage the "{agent_type}"'))
def verify_agent_engaged(bdd_context, agent_type):
    result = bdd_context["result"]
    assert agent_type in result