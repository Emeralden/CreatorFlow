# CreatorFlow

An autonomous AI content production engine built for the Google Cloud Gen AI Academy APAC Hackathon.
Powered by Gemini 2.5 Flash + Google ADK multi-agent orchestration + MCP-to-Postgres execution.

[![API Service](https://img.shields.io/badge/Live-App-brightgreen)](https://creatorflow-webapp-818053237817.us-central1.run.app/dev-ui)
[![Web UI Service](https://img.shields.io/badge/API-Docs-blue)](https://creatorflow-webapp-818053237817.us-central1.run.app/docs)

---

## The Vision
Content creation today is marked by inefficiency and fragmentation. Creators frequently shift between scripting, task management, and filming schedules, leading to constant context switching.

**CreatorFlow** is a Multi-Agent system that turns a single natural language prompt into a fully persisted production pipeline. It doesn't just "suggest", but it **executes**.

---

## Why this isn’t “just a chatbot”
I stopped building chatbots. I built an AI operating system instead.

Read the write-up: https://medium.com/@7ksb24/i-stopped-building-chatbots-i-built-an-ai-operating-system-instead-5100272b26fc

---
## The Architecture
CreatorFlow is built on a strictly hierarchical **Multi-Agent Orchestration** pattern using the **Google ADK**.

### **1. The Brain: Primary Orchestrator**
*   **Role:** The Root agent.
*   **Logic:** Analyzes intent and delegates to specialized sub-agents. 
*   **Zero-Friction Identity:** Automatically manages session-based identity using `uuid` injection.

### **2. The Sub-Agents**
*   **`project_handler`**: Handles projects, tasks and scripts management.
*   **`production_manager`**: Helps in ISO-standard scheduling sessions.
*   **`status_tracker`**: Used for relational data retrieval and unified views.

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
