# CreatorFlow

### **The Autonomous AI Content Production Engine**
*Built for the Google Cloud Gen AI Academy APAC Hackathon*

[![API Service](https://campuscue-agent-creatorflow-818053237817.us-central1.run.app)
[![Web UI Service](https://creatorflow-webapp-818053237817.us-central1.run.app)

---

## 🌟 The Vision
Content creation is broken. Creators spend lot of their time context-switching between scripts, tasks, and filming slots. 

**CreatorFlow** is a Multi-Agent system that turns a single natural language prompt into a fully persisted production pipeline. It doesn't just "suggest", but it **executes**.

---

## The Architecture
CreatorFlow is built on a strictly hierarchical **Multi-Agent Orchestration** pattern using the **Google ADK**.

### **1. The Brain: Primary Orchestrator**
*   **Role:** The Root agent.
*   **Logic:** Analyzes intent and delegates to specialized sub-agents. 
*   **Zero-Friction Identity:** Automatically manages session-based identity using `uuid` injection.

### **2. The Specialists: Sub-Agents**
*   **`project_handler`**: Specialist in projects, tasks and scripts management.
*   **`production_manager`**: Specialist in ISO-standard scheduling sessions.
*   **`status_tracker`**: Specialist in relational data retrieval and unified views.

### **3. The Body: Model Context Protocol (MCP)**
*   **Secure Bridge:** Uses the Google `genai-toolbox` to connect LLM reasoning to raw SQL execution.
*   **Relational Integrity:** Executes complex **CTE (Common Table Expressions)** and **UPSERT** logic to keep 5 interconnected PostgreSQL tables in sync.

---

## Tech Stack
*   **LLM:** Gemini 2.5 Flash (Ultra low-latency tool calling)
*   **Framework:** Google Agent Development Kit (ADK)
*   **Integration:** Model Context Protocol (MCP)
*   **Database:** Neon PostgreSQL (Relational persistence)
*   **Infrastructure:** Google Cloud Run (Stateless containerized scaling)

---

## Key Features
*   **Autonomous Multi-Step Workflows:** Create a project, write a script, and schedule filming in ONE prompt.
*   **Self-Healing Schema:** Automatically ensures database tables exist on boot via MCP.
*   **Strict Tool Isolation:** Sub-agents only see the tools they need, eliminating hallucinations.
*   **Production-Ready Logging:** Full execution tracing via the ADK Dev UI.
