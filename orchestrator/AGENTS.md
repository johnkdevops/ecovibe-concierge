# AGENTS.md - EcoVibe Concierge

This file defines the agent configuration for Antigravity.

## Main Agent: Orchestrator

**Name**: ecovibe-orchestrator  
**Description**: Central coordinator for the 4-agent EcoVibe Concierge system.  
**Model**: gemini-3.5-flash-medium  
**Temperature**: 0.65  
**Max Tokens**: 8192

### Skills Used
- tracker-skill
- researcher-skill
- planner-skill

### Tools
- emission_calculator

### System Prompt
See: `orchestrator/SKILL.md`

---

## Specialist Agents

### Tracker Agent
**Path**: skills/tracker-skill/SKILL.md  
**Role**: Carbon footprint calculations and tracking

### Researcher Agent
**Path**: skills/researcher-skill/SKILL.md  
**Role**: Grounded research and data retrieval

### Planner Agent
**Path**: skills/planner-skill/SKILL.md  
**Role**: Personalized planning and goal setting

---

## Memory Configuration
- Long-term user profile stored in `memory/user_profile.json`
- Session memory managed by Orchestrator

## Activation Instructions
Use in Antigravity:
```bash
antigravity run --agent orchestrator/agent.json