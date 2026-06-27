# EcoVibe Concierge – Multi-Agent Sustainability Assistant

**A 4-Agent AI System built with Google Antigravity, Vertex AI & Gemini**  
*Capstone Project – 5-Day AI Agents Intensive Vibe Coding Course with Google*

![EcoVibe Banner](https://via.placeholder.com/800x200?text=EcoVibe+Concierge)

## Overview

EcoVibe Concierge is a **personal sustainability companion** powered by a team of 4 specialized AI agents. It tracks your carbon footprint, provides grounded recommendations, creates personalized eco-plans, and helps you reduce your environmental impact — all while maintaining safety, privacy, and human oversight.

It demonstrates **end-to-end agentic development** using techniques from all 5 days of the course.

## The 4-Agent Team

| Agent           | Role                                      | Key Responsibilities                     |
|-----------------|-------------------------------------------|------------------------------------------|
| **Orchestrator**   | Team Lead / Coordinator                  | Routing, memory, safety, final response |
| **Tracker**        | Calculation Specialist                   | Carbon footprint calculations & tracking         |
| **Researcher**     | Grounding & Insights Specialist          | Web search, fact-checking, alternatives |
| **Planner**        | Personalization & Action Specialist      | Weekly plans, goal tracking, Calendar integration   |

## Features

- Natural conversation interface
- Real-time carbon footprint tracking
- Grounded recommendations with citations
- Personalized weekly and monthly eco-plans
- Long-term user memory (habits, preferences, goals)
- Human-in-the-loop approvals for sensitive actions
- Safety guardrails and observability

## Tech Stack

- **Framework**: Google Antigravity IDE + CLI + ADK
- **Models**: Gemini 3.5 Flash (Medium)
- **Environment Management**: uv (with shared cache)
- **Deployment**: Cloud Run + Vertex AI Agent Engine
- **Tools**: Custom emission calculator, Google Search grounding, optional Maps/Calendar
- **Skills**: Custom 'SKILL.md' files + Antigravity Skills (planning, research, orchestration, etc.)

## Project Structure

```bash
ecovibe-concierge/
├── .env                  # Environment secrets (API Keys, GCP details)
├── .gitignore            # Excludes dependencies, Python caches, and state logs
├── .python-version       # Virtual environment Python engine definition (3.12.13)
├── LICENSE.md            # Open-source compliance mapping
├── main.py               # Active central gateway & routing backend (FastAPI)
├── pyproject.toml        # Declarative uv-compatible dependency manifest
├── README.md             # Project roadmap & operational instructions
├── uv.lock               # Cryptographically pinned lockfile for reproducibility
│
├── deployment/           # Day 5 Production Containerization
│   ├── Dockerfile        # Multi-stage optimized build file
│   └── cloud-run.yaml    # Declarative Cloud Run deployment manifest
│
├── memory/               # Context Persistence Subsystem
│   ├── memory_manager.py # I/O interface for profile management
│   └── user_profile.json # Active user preference & footprint tracking state
│
├── orchestrator/         # Day 3 Agentic Definition Manifests
│   ├── AGENTS.md         # Multi-agent system orchestration definitions
│   └── SKILLS.md         # Pluralized agentic prompt/skill definition
│
├── scripts/              # Local Diagnostic Tools
│   └── models.py         # Model discovery and validation tester
│
├── skills/               # Specialist Agent Architectures
│   ├── planner-skill/
│   │   └── SKILL.md      # Goal setting, schedules, and personalized calendar prompts
│   ├── researcher-skill/
│   │   └── SKILL.md      # Grounded Search context instructions
│   └── tracker-skill/
│       └── SKILL.md      # Mathematical processing instructions
│
└── tools/                # Business Math & Core API Implementations
    └── emission_calculator.py
```

---

## 🚀 Quick Start (Windows 10 + Git Bash)


### Prerequisites
- Google AI Pro membership
- Antigravity App + Antigravity IDE + Antigravity CLI installed
- Git Bash
- uv installed
- Google Cloud Project with Vertex AI API enabled
- Google AI Studio API Key (Free or Paid)

### Setup Steps
```bash
# 1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/ecovibe-concierge.git
cd ecovibe-concierge

# 2. Set shared uv cache (recommended)
export UV_CACHE_DIR="/c/KodeKloud_Pro/Google_Cloud/5-Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/uv-cache"

# 3. Install Python 3.12 (only once)
uv python install 3.12

# 4. Pin Python version for this project
uv python pin 3.12.13

# 5. Create & activate virtual environment
uv venv 
source .venv/Scripts/activate

# 6. Install dependencies
uv sync
uv sync --extra dev

# 7. Configure Environment Variables
cp .env.example .env
# Edit .env with your API keys and GOOGLE_CLOUD_PROJECT
```

### Run the Application
```bash
# Recommended: Run with Antigravity
antigravity run

# Alternative: Direct run
uv run python main.py 
```

### Clean Shutdown (free up resources)
```bash
deactivate
rm -rf .venv
```

---

## Development Workflow

### Start session
```bash
cd /c/KodeKloud_Pro/Google_Cloud/5-Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/ecovibe-concierge
export UV_CACHE_DIR="/c/KodeKloud_Pro/Google_Cloud/5-Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/uv-cache"
uv venv
source .venv/Scripts/activate
uv sync
uv sync --extra dev
```

### End session
```bash
deactivate
rm -rf .venv
```

---

## Deployment

- **Prototype**: Cloud Run
- **Production**: Vertex AI Agent Engine

### Deployment (Cloud Run)

# 1. Build & Deploy
```bash
# Build and push
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ecovibe-concierge .

# 2. Deploy to Cloud Run
gcloud run deploy ecovibe-concierge \
  --image gcr.io/YOUR_PROJECT_ID/ecovibe-concierge \
  --platform managed \
  --region YOUR_REGION \
  --allow-unauthenticated \
  --port 8080
``` 

---
## Architecture & Course Mapping
This project explicitly demonstrates techniques from all 5 days of the course:

- **Day 1**: Vibe coding in Antigravity + initial Cloud Run deployment
- **Day 2**: Tools, APIs, and agent-to-agent communication
- **Day 3**: SKILL.md specialist agents + memory + planning
- **Day 4**: Security, guardrails, human-in-the-loop, evaluation
- **Day 5**: Production deployment + observability

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- John Kennedy - AI Engineer
- 4 AI Agents - Orchestrator, Tracker, Researcher, Planner

##  🙏 Acknowledgments

- Google Antigravity Team - For the amazing IDE and tools
- Vertex AI Team - For the powerful AI platform

## 🔗 Links

- [Google Antigravity](https://antigravity.dev/)
- [Vertex AI](https://cloud.google.com/vertex-ai)

---

**Built with ❤️ using Google Antigravity and Vertex AI**
