"""
EcoVibe BDD Step Verification Suite
Validates Day 5 Spec-Driven Development (SDD) compliance.
Run locally with: pytest tests/test_agent_routing.py
"""

import json
import pytest
from unittest.mock import MagicMock
from main import AgenticOrchestrator

# Create a mock schema generator matching the orchestrator's output
def mock_gemini_routing_call(category: str):
    mock_response = MagicMock()
    mock_response.text = json.dumps({"category": category})
    return mock_response

@pytest.fixture
def orchestrator():
    orchestrator_instance = AgenticOrchestrator()
    # Mock the client generate content sequence
    orchestrator_instance.client = MagicMock()
    return orchestrator_instance

def test_emissions_routing_trajectory(orchestrator):
    # Given the EcoVibe Orchestrator is initialized and active
    # When the user submits the message "I drove 45 miles today in my gasoline car"
    user_input = "I drove 45 miles today in my gasoline car"
    
    # Mock routing output from primary LLM
    orchestrator._generate_with_fallback = MagicMock(
        return_value=mock_gemini_routing_call("TRACK_EMISSIONS")
    )
    
    # Mock agent execution output to bypass missing live MCP contexts during tests
    orchestrator._handle_mcp_tracking = MagicMock(
        return_value="### 🚗 Tracker Agent (Firebase Core)\nEmission logged successfully in Firestore."
    )
    
    # Then the system should categorize the request trajectory as "TRACK_EMISSIONS"
    result = orchestrator.process(user_input)
    
    # And the dispatch logic should engage the Tracker Agent
    assert "TRACK_EMISSIONS" in orchestrator._generate_with_fallback.call_args[1]["contents"]
    assert "Tracker Agent" in result
    assert "logged successfully in Firestore" in result

def test_research_routing_trajectory(orchestrator):
    # Given the EcoVibe Orchestrator is initialized and active
    # When the user submits the message "Research the environmental benefits of electric vehicles"
    user_input = "Research the environmental benefits of electric vehicles"
    
    # Mock routing output from primary LLM
    orchestrator._generate_with_fallback = MagicMock(
        return_value=mock_gemini_routing_call("RESEARCH")
    )
    
    # Mock agent execution output
    orchestrator._handle_mcp_research = MagicMock(
        return_value="### 🔍 Researcher Agent (Knowledge Base)\nResearch complete."
    )
    
    result = orchestrator.process(user_input)
    
    # Assertions for research path
    assert "RESEARCH" in orchestrator._generate_with_fallback.call_args[1]["contents"]
    assert "Researcher Agent" in result