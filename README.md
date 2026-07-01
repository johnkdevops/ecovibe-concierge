# **🌱 EcoVibe Concierge – Multi-Agent Sustainability Assistant**

**A Production-Grade 4-Agent Swarm System with Live Cloud Integration & Spec-Driven Testing**

*Capstone Project – 5-Day AI Agents Intensive Vibe Coding Course with Google*

## **🎯 Asymmetric Portfolio Advantage (Solo vs. 5-Member Teams)**

While multi-member teams suffer from high communication overhead, branch conflicts, and monolithic designs, **EcoVibe Concierge** demonstrates elite software engineering velocity:

1. **Decoupled Architecture**: Separation of presentation (templates/), hosting (main.py), and reasoning (orchestrator.py) limits cross-module side effects.  
2. **Deterministic & Semantic Hybrids**: Combines LLM-driven intent classification with absolute mathematical calculations ($0.411\text{ kg CO}_2\text{e/mile}$ for driving) to prevent semantic calculation drift.  
3. **Automated BDD Quality Gates**: Verified by an isolated Gherkin test engine (pytest-bdd) that proves core routing accuracy before executing expensive cloud API tokens.

## **👥 The 4-Agent Swarm Matrix**
```bash
       \[ User Query \]  
              │  
              ▼  
   ┌──────────────────────┐  
   │  Orchestrator Agent  │ \<──► \[ Long-Term memory / User Session \]  
   └──────────┬───────────┘  
              │ (Routes Semantic Trajectory)  
              ├─────────────────────────┼─────────────────────────┐  
              ▼                         ▼                         ▼  
     ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐  
     │  Tracker Agent  │       │Researcher Agent │       │  Planner Agent  │  
     └────────┬────────┘       └────────┬────────┘       └────────┬────────┘  
              │                         │ (Google Search)         │ (Calendar/Goals)  
              ▼ (Direct gRPC)           ▼                         ▼  
    \[(default) Firestore\]      \[ Grounded Citations\]     \[Human-In-The-Loop\]
```

| Agent | Core Domain | Capstone Technical Highlights |
| :---- | :---- | :---- |
| **Orchestrator** | Team Lead / Coordinator | Single-point ingress, system guardrails, context assembly, multi-model high-availability fallbacks (gemini-3.5-flash &rarr; gemini-2.5-flash). |
| **Tracker** | Calculation Specialist | Ingests conversational trip descriptions, calculates precise footprints, and commits structured ledger schemas to live Google Cloud Firestore. |
| **Researcher** | Grounding Specialist | Executes dynamic lookup loops backed by official search grounding tools to deliver real-time, peer-reviewed eco-alternatives with full citations. |
| **Planner** | Personalization Specialist | Generates hyper-personalized actionable carbon offset goals, managing human-in-the-loop approvals for external calendar insertions. |

## **🛠️ Tech Stack & Architecture**

* **Backend Gateway**: FastAPI (v0.110.0+) with absolute-path self-healing asset mapping.  
* **Frontend Layer**: Jinja2 Template Engine displaying dynamic server-side host parameters and interactive Tailwind CSS panels.  
* **Agent Orchestration**: Native google-genai SDK combined with specialized semantic routing logic.  
* **Database Layer**: Production-grade native google-cloud-firestore direct clients (guaranteeing secure, thread-safe write channels).  
* **External Integration (MCP)**: Decoupled Cloud-Hosted Model Context Protocol (SSE-based Developer Knowledge Server) completely eliminating local Windows terminal popups.  
* **Test Engine**: pytest-bdd parsing declarative Gherkin specs and injecting mock client sandboxes.

## **📁 Project Directory Map**

ecovibe-concierge/  
├── .agents/                   
│   └── mcp\_config.json      \# SSE Cloud MCP Grounding Server Configurations  
├── .env                     \# Target Cloud Project Profiles & Secret Port Definitions  
├── .python-version          \# Lock to Python CPython 3.12.13  
├── main.py                  \# HTTP API Service Layer (FastAPI & Jinja2 Mounting)  
├── orchestrator.py          \# Isolation Core: Semantic Trajectory Router & Firestore Client  
├── pyproject.toml           \# Unified Project Meta-manifest & Pytest systempath overrides  
├── README.md                \# Senior Evaluator Overview & Execution Roadmap  
├── uv.lock                  \# Pinned cryptographic environment dependencies  
│  
├── scripts/                   
│   └── eco-stop.sh          \# Force-teardown utility for Windows/Git Bash port release  
│  
├── templates/                 
│   └── index.html           \# Live Interactive Jinja2 Frontend (Responsive Tailwind UI)  
│  
└── tests/                   \# BDD Spec-Driven Quality Suite  
    ├── features/  
    │   └── agent\_routing.feature  \# Physical Gherkin Declarative Routing Specs  
    └── test\_agent\_routing.py      \# pytest-bdd step assertions & GenAI Mock fixtures

## **🚀 Rapid Local Setup & Verification**

Follow these steps to run the application and execute the behavior-driven verification suite in Git Bash on Windows:

### **1\. Synchronize Dependencies**

This project uses the hyper-fast uv package manager with a standardized workspace cache:

\# Set shared cache directory (if required)  
export UV\_CACHE\_DIR="./uv-cache"

\# Auto-provision virtual environment and synchronize dependencies  
uv sync  
source .venv/Scripts/activate

### **2\. Verify Behavioral Specifications (BDD)**

Confirm the orchestrator's routing compliance using the native Gherkin parser before spinning up local servers:

python \-m pytest tests/test\_agent\_routing.py

*Both routing trajectories (Tracking vs. Research) must return green checkmarks ($100\%$ passed).*

### **3\. Launch the Application**

Start the service in hot-reload developer mode:

uv run python main.py

Open **http://localhost:8080** to access the dynamic workspace dashboard. The header badges will automatically query and display your active GCP project credentials\!

### **4\. Safe Shutdown Utility**

On Windows systems, terminal processes can occasionally lock up active web ports. Kill the server and release the network binds cleanly by running:

bash scripts/eco-stop.sh

## **🧪 BDD Gherkin Specifications**

The system is continuously verified against the following declarative behaviors:

Feature: EcoVibe Concierge \- Orchestrator Routing Verification

  Scenario: A user logs emissions data  
    Given the EcoVibe Orchestrator is initialized and active  
    When the user submits the message "I drove 45 miles today in my gasoline car"  
    Then the system should categorize the request trajectory as "TRACK\_EMISSIONS"  
    And the dispatch logic should engage the "Tracker Agent"

  Scenario: A user requests sustainability research and grounding  
    Given the EcoVibe Orchestrator is initialized and active  
    When the user submits the message "Research the environmental benefits of electric vehicles"  
    Then the system should categorize the request trajectory as "RESEARCH"  
    And the dispatch logic should engage the "Researcher Agent"

## **🤝 Team & Acknowledgments**

* **Lead AI Engineer**: John Kennedy  
* **Orchestration Matrix**: Orchestrator, Tracker, Researcher, Planner (Autonomous Agents)  
* **Course Director**: Google Cloud 5-Day Intensive Vibe Coding Team

*Built with ❤️ in Google Antigravity to deliver sustainable engineering excellence.*



