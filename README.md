# **🌱 EcoVibe Concierge – Multi-Agent Sustainability Assistant**

**A Production-Grade 3-Agent Swarm System with Live Cloud Integration, Zero-Trust IAM, & Dual-Mode Red-Team Auditing**

*Solo Capstone Portfolio Project – 5-Day AI Agents Intensive Vibe Coding Course with Google*

## **🎯 Asymmetric Portfolio Advantage (Solo vs. 5-Member Teams)**

While multi-member teams suffer from high communication overhead, branch conflicts, and monolithic bottlenecks, **EcoVibe Concierge** demonstrates elite software engineering velocity and decoupled design:

1. **Decoupled Architecture**: Absolute separation of presentation (`templates/`), server hosting (`main.py`), and multi-agent reasoning (`modules/orchestrator.py`) to eliminate cross-module side effects.  
2. **Deterministic & Semantic Hybrids**: Combines LLM-driven intent classification with strict mathematical coefficients (e.g., $0.411 \text{ kg CO}_2\text{e}$ per mile for gasoline driving) to prevent semantic calculation drift or database poisoning.  
3. **Automated BDD & Live Adversarial Quality Gates**: Verified by both an offline Gherkin test engine (`pytest-bdd`) and a live, over-the-wire HTTP Red-Team test suite (`pytest`) to audit live staging deployments before atomic promotion.  
4. **Keyless Zero-Trust Security**: Employs native GCP Service Account bindings (`roles/datastore.user` and `roles/aiplatform.user`) to communicate natively with Firestore and Vertex AI, completely eliminating hardcoded API keys from the container images.

## Prerequisites

1. **Workstation Dependencies (Local Box)**
- **Operating System:** Windows 10/11 (Git Bash terminal recommended).
- **Antigravity IDE:** Antigravity IDE installed and configured.
- **Python Runtime:** Python `3.12.13` (Hard-locked via `.python-version`).
- **Package Engine:** `uv` package manager (v0.5.0+) for lightning-fast lockfile synchronizations and virtual environment isolation.
- **GCP Command Line:** Google Cloud SDK (`gcloud`) installed, authenticated, updated, and configured to use the project `ecovibe-concierge`.

2. **Google Cloud Platform (GCP)**
- **Active GCP Project:** A valid, uniquely named GCP project (e.g., `ecovibe-project`).
- **Active Billing Profile:** A Google Cloud Billing Account linked to your project. To utilize the required container hosting and Vertex AI models keyless, **your project must be configured on the Blaze (Pay-as-you-go) plan.**
- **Firestore Database:** Created and configured in the `ecovibe-project` project.
- **Google Service Account:** A secure, custom GCP Service Account with least-privilege IAM roles mapped to target databases and AI suites. 
- **API Keys:**
  - **Gemini API Key:** Obtained from [Google AI Studio](https://aistudio.google.com/app/apikey).
    - **Google API Key Free Tier:** [Google AI Studio Free Tier](https://aistudio.google.com/app/apikey). Project i.e. `eco-vibe-sandbox`
    - **Google API Key Paid Tier:** [Google AI Studio Paid Tier](https://aistudio.google.com/app/apikey). Project i.e. `eco-vibe-project`

## **👥 The 3-Agent Swarm Matrix**


       [ User Query ]    
              │    
              ▼       
    [ Orchestrator Agent ] <──► [ Long-Term Memory (Local Cache) ]    
       
              │ (Routes Semantic Trajectory)    
              ├─────────────────────────┐    
              ▼                         ▼    
     ┌─────────────────┐       ┌─────────────────┐    
     │  Tracker Agent  │       │Researcher Agent │    
     └────────┬────────┘       └────────┬────────┘    
              │                         │ (Google Search Tool)    
              ▼ (Direct Secure gRPC)    ▼    
     [ Cloud Firestore ]       [ Grounded Citations ]



| Agent | Core Domain | Capstone Technical Highlights |
| :---- | :---- | :---- |
| **Orchestrator** | **Team Lead / Router** | Handles pre-flight safety analysis, user context assembly, and semantic routing decisions with multi-model fallback mechanics (`gemini-3.5-flash` &rarr; `gemini-2.5-flash`). |
| **Tracker** | **Calculation Specialist** | Ingests freeform chat, extracts metadata parameters, applies strict backend physical limits, and writes verified schema records securely to Cloud Firestore. |
| **Researcher** | **Knowledge Grounder** | Executes real-time Google Search grounding loops to return peer-reviewed eco-alternatives with citations, resolving data accuracy limits. |

## **🛠️ Tech Stack & Architecture**

* **Backend Gateway**: FastAPI with absolute-path self-healing asset mapping and **SlowAPI** IP rate limiting (Denial-of-Wallet mitigation).  
* **Frontend Layer**: Jinja2 Template Engine displaying dynamic server host configurations, styled with responsive Tailwind CSS panels.  
* **Agent Orchestration**: Native Google `google-genai` SDK combined with custom JSON schema structures.  
* **Database Layer**: Production-grade Google Cloud Firestore running thread-safe native client sessions.  
* **External Integration**: Decoupled, cloud-hosted Model Context Protocol (SSE-based Developer Knowledge Server) eliminating local dependency bottlenecks.  
* **Defense Architecture**: Programmatic uvicorn-layer rate limiting paired with container-level scaling constraints (`maxScale: "1"`).

## **📁 Project Directory Map**

ecovibe-concierge/    
├── .agents/                       
│   └── mcp\_config.json        \# SSE Cloud MCP Grounding Server credentials    
├── deployment/    
│   ├── Dockerfile             \# Production-ready multi-stage Debian-Slim build blueprint    
│   └── cloud-run.yaml         \# Declarative Knative layout (scaling caps, IAM Service Account binds)    
├── memory/    
│   ├── memory\_manager.py      \# Thread-safe profile loading and footprint state persistence    
│   └── user\_profile.json      \# Long-term contextual parameters (habits, history)    
├── modules/    
│   └── orchestrator.py        \# Core Engine: Safety Gateway, Intent Router & Agent Dispatcher    
├── scripts/    
│   ├── setup-iam.sh           \# Shell script to auto-provision IAM roles & custom Service Account    
│   └── eco-stop.sh            \# Safe Windows port clean-up utility    
├── templates/    
│   └── index.html             \# Live responsive Tailwind UI mounted via Jinja2 templates    
├── tests/    
│   ├── features/    
│   │   └── agent\_routing.feature     \# Declarative Gherkin test scenarios    
│   ├── test\_agent\_routing.py         \# Pytest-bdd step assertions & routing verifications    
│   ├── test\_red\_team\_simulation.py   \# Offline, fully sandboxed adversarial security test suite    
│   └── test\_red\_team\_simulation\_green.py \# Live HTTP over-the-wire green staging testing suite    
├── .env                       \# Local developer secret profile targets    
├── main.py                    \# Gateway app runner (fastapi, SlowAPI, template engine mounting)  
├── Dockerfile                 \# Production-ready multi-stage Debian-Slim build blueprint
├── pyproject.toml             \# Unified modern python build-system dependencies    
└── README.md                  \# Comprehensive Capstone handbook and runbook

## **⚡ Step-by-Step GCP & Native Firestore Provisioning Guide**

Execute these commands inside your terminal workspace to configure your Google Cloud project services and spin up your live, enterprise-grade cloud database instance:

### **1\. Authenticate & Configure Target Project & Clone Repo**

Ensure your local gcloud context is authenticated and pinned directly to your active project space:

```bash
# 1. Clone the repository & cd into it & copy .env.example to .env
git clone https://github.com/johnkdevops/ecovibe-concierge.git
cd ecovibe-concierge
cp .env.example .env

# 2. Authenticate terminal environment  
gcloud auth login

# 3. Set active working project (Replace with your actual project ID)  
gcloud config set project eco-vibe-project
```

### **2\. Enable Required Google Cloud Service APIs**

Activate the structural APIs required to allow your serverless container to interact with Vertex AI, Google Search Grounding networks, and Cloud Firestore:

```bash
# Enable Firestore, Vertex AI (Platform), and Cloud Build APIs  
gcloud services enable \
    firestore.googleapis.com \
    aiplatform.googleapis.com \
    cloudbuild.googleapis.com \
    run.googleapis.com \
    --project=eco-vibe-project
```

### **3\. Provision Native Cloud Firestore (GCP / Firebase Core)**

To establish database connections for the Tracker Agent, you must create a Firestore database instance. Cloud Run requires a database configured in **Native Mode**:

```bash
# Provision the default database instance in Firestore Native mode  
gcloud firestore databases create \  
    --location=us-east1 \  
    --type=firestore-native \  
    --project=eco-vibe-project
```

*Note: The --location flag must match your deployment regional footprint (e.g., us-east1 or us-central1) to ensure optimal latency and zero multi-regional egress billing.*

## **🚀 Rapid Local Setup & Verification**

Execute these steps in your local **Git Bash** terminal on Windows to compile dependencies and run behavior-driven test verifications.

### **1\. Synchronize Dependencies**

This project uses the modern, lightning-fast `uv` package manager with a standardized workspace cache:

```bash
# Set shared cache directory  
export UV_CACHE_DIR="./uv-cache"

# Provision virtual environment and synchronize dependencies in one step  
uv sync && uv sync --extra dev 
source .venv/Scripts/activate
```

### **2\. Run Behavior-Driven (BDD) Tests**

Validate your Gherkin routing behaviors locally before invoking live cloud tokens:

```bash
python -m pytest tests/test_agent_routing.py -v
```

*Both routing trajectories (Tracking vs. Research) must return green checkmarks (![][image2] passed).*

### **3\. Start Local Developer Server**

Launch the FastAPI microservice locally:

```bash
uv run python main.py
```

*Open **http://localhost:8080** to view your interactive Tailwind CSS workspace dashboard.*

### **4\. Safe Shutdown Utility**

On Windows systems, terminal processes can occasionally lock up active web ports. Kill the server and release the network binds cleanly by running:

```bash
bash scripts/eco-stop.sh
```

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

## **🛠️ Development Workflow & Cloud Native Provisioning**

### **1\. Start Session & Authenticate**

Navigate to the project root and authenticate with Google Cloud:

```bash
cd /c/KodeKloud_Pro/Google_Cloud/5-Day_AI_Agents_Intensive_Vibe_Coding_Course_With_Google/ecovibe-concierge  
gcloud auth login  
PROJECT_ID=eco-vibe-project  
gcloud auth application-default set-quota-project $PROJECT_ID
```

### **2\. Setup Custom IAM Identity**

Trigger the setup script to create the custom service account and bind Firestore and Vertex AI permissions securely:

```bash
chmod +x scripts/setup-iam.sh  
./scripts/setup-iam.sh
```

### **3\. Enable APIs & Build Container**

Enable the necessary Vertex AI endpoints and compile the container image remotely using Google Cloud Build:

```bash
# Enable the Vertex AI API  
gcloud services enable aiplatform.googleapis.com --project=eco-vibe-project

# Compile the self-healing container image  
gcloud builds submit --tag gcr.io/eco-vibe-project/ecovibe-concierge:latest .
```

### **4\. Deploy To Cloud Run**

Push your Knative deployment live using the declarative configuration template:

```bash
# Push Knative deployment live with custom identity  
gcloud run services replace deployment/cloud-run.yaml --region=us-east1

# Alternatively, force Cloud Run to deploy a fresh revision from the registry  
gcloud run deploy ecovibe-concierge \\  
    --image=gcr.io/eco-vibe-project/ecovibe-concierge:latest \\  
    --region=us-east1

# (Optional) Tail live Cloud Run logs in Git Bash to watch the container boot  
gcloud run services logs read ecovibe-concierge --region=us-east1 --limit=100
```

## **🛡️ Red-Team Adversarial Quality Audits**

### **Local Sandboxed Verification (Offline)**

Verify that your system prompt guardrails, out-of-bounds metrics checks, and database injection sanitizations behave cleanly in a local mock sandbox:

```bash
python -m pytest tests/test_red_team_simulation.py -v -s
```

### **Staging Over-The-Wire Verification (Live HTTP)**

Verify safety rules directly against your active, live cloud-deployed endpoints. Set your staging destination inside your configuration profile and run:

```bash
# Point your target URL to your live Cloud Run instance  
export TARGET_URL="https://ecovibe-concierge-{build-id}.us-east1.run.app" or
add to .env file

# Execute live HTTP adversarial and connection flood checks  
python -m pytest tests/test_red_team_simulation_green.py -v -s
```

## **🚙 Live Blue/Green Staging & Promotion Runbook**

Deploy silent staging revisions, audit them over-the-wire, and promote them atomically to production with zero downtime.

```
                   [ Public Users (Root Production URL) ]  
                                      │  
                                      ▼  
                        [ Cloud Run Traffic Router ]  
                                      │  
            ┌─────────────────────────┴─────────────────────────┐  
            │ 100% (Production Traffic)                         │ 0% (Staged/Testing Traffic)  
            ▼                                                   ▼  
   [ Revision: BLUE (Active Production App) ]         [ Revision: GREEN New release being QA'd: 
                                                       Custom Tag: "green" ]
```   

### **Step 1: Deploy Green Revision Silently**

Deploy the new revision image silently with **0% public traffic** routed to it, bound to the custom tag green:

```bash
gcloud run deploy ecovibe-concierge \
    --image=gcr.io/eco-vibe-project/ecovibe-concierge:latest \
    --region=us-east1 \
    --platform=managed \
    --no-traffic \
    --tag=green
```

*This generates a dedicated isolation URL: `https://green---ecovibe-concierge-{build-id}.us-east1.run.app*`

### **Step 2: Bind credentials and run audits**

Bind the environment parameters to the Green revision block and execute live Red-Team verification loops:

```bash
# Add the Gemini API Key configuration to the green environment  
gcloud run services update ecovibe-concierge \
    --region=us-east1 \
    --set-env-vars=GEMINI_API_KEY="{Enter your GEMINI_API_KEY}",ENVIRONMENT="production"

#    Direct over-the-wire live tests to target the green URL  
export TARGET_URL="https://green---ecovibe-concierge-1054134335986.us-east1.run.app"  or from .env file
python -m pytest tests/test_red_team_simulation_green.py -v -s
```

### **Step 3: Atomic Promotion**

Once the Green deployment passes all tests (6/6 passed), list the active revisions to identify the targeted revision name:

```bash
gcloud run revisions list --service=ecovibe-concierge --region=us-east1
```

Route 100% of production traffic instantly to the root vanity domain URL (https://ecovibe-concierge-{build-id}.us-east1.run.app/):

```bash
# Swing traffic atomically to your clean target Revision ID  
gcloud run services update-traffic ecovibe-concierge \
    --region=us-east1 \
    --to-revisions=ecovibe-concierge-00007-piy=100
```

### **Step 4: Clean Up Inactive Revisions**

Delete old, stale, or quota-exhausted Blue revisions to leave your Cloud Console clean and cost-optimized:

```bash
# Delete targeted legacy revision  
gcloud run revisions delete ecovibe-concierge-00002-qht --region=us-east1 --quiet
```

## **🔧 Cleanup & Workspace Teardown**

If you need to completely tear down your cloud resources, run the following commands:

```bash
# 1. Delete the Cloud Run service  
gcloud run services delete ecovibe-concierge --region=us-east1 --quiet

# 2. Delete the container image from registry  
gcloud container images delete gcr.io/eco-vibe-project/ecovibe-concierge:latest --quiet

# 3. Delete the Firestore database (WARNING: This permanently wipes all user tracking ledgers!)
gcloud firestore databases delete --database="(default)" --project=eco-vibe-project --quiet

# 4. Delete the service account  
gcloud iam service-accounts delete ecovibe-run-sa@eco-vibe-project.iam.gserviceaccount.com --quiet

# 5. Stop local port binds and background process locks  
bash scripts/eco-stop.sh
```

## **🤝 Team & Acknowledgments**

* **Lead Cloud AI Architect**: John Kennedy  
* **Orchestration Matrix**: Orchestrator, Tracker, Researcher (3-Agent Swarm System)  
* **Evaluator Board**: Google Cloud 5-Day Intensive Vibe Coding Team

*Built with ❤️ in Google Antigravity to deliver sustainable cloud-native engineering excellence.*

