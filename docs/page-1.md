
# 📄 High-Level Overview

## 1. Purpose & Goals

**Purpose:**
Build an **agentic AI system** that uses **Gemini (LLM + Vision)**, **weather intelligence (OpenMeteo)**, and **domain knowledge (Chroma vector store)** to:

* Diagnose crop issues from images.
* Combine that with weather & field context.
* Generate **structured, JSON-only, 7-day treatment plans**.
* Support **multiple crops** in a realistic, Syngenta-like workflow.

**Goals:**

* Showcase a **multi-agent, branching LangGraph pipeline** using real APIs.
* Demonstrate how **GenAI + agents** can augment agronomists and farmers.
* Be strong enough as a **flagship portfolio project** for Syngenta interviews:

  * Clean architecture
  * Agentic pipeline
  * Domain reasoning (agronomy)
  * Multi-crop support

---

## 2. Target Users

* **Primary (for interview/demo):**

  * Syngenta interviewers (R&D / Digital Ag / AI roles)
  * Agronomy/data-science teams evaluating your system thinking

* **Secondary (real-world personas):**

  * **Farmers / Field Officers:** capture images, get recommendations.
  * **Agronomists:** review / override AI-generated plans.
  * **Sales / Product Advisors:** use recommendations to support product advisory (without real brand names in your project).

---

## 3. Overall System Architecture

**Key Components:**

* **Frontend:** React + Tailwind single-page app.
* **Backend API:** FastAPI.
* **Agent Orchestration:** LangChain + LangGraph (branching, multi-agent).
* **LLM & Vision:** Gemini API (text + vision).
* **Weather Data:** OpenMeteo API (all supported vars you selected).
* **Database:**

  * **SQLite** (fields, users, runs, crops, logs).
  * **Chroma** vector store (disease/pest knowledge base, crop profiles, FAQs).

### Architecture Flow (Conceptual)

```text
[React Frontend]  <--->  [FastAPI Backend]

FastAPI calls:
   └── LangGraph workflow:
        ├── Vision Agent (Gemini Vision API)
        ├── Weather Agent (OpenMeteo API)
        ├── Field Context Agent (RAG over Chroma)
        ├── Reasoning Agent (Gemini Text API)
        ├── Planner Agent (Gemini Text API, branching logic)

Data:
   ├── SQLite (entities, jobs, results, crops)
   └── Chroma (embedded agronomy knowledge)
```

---

## 4. High-Level Workflow

1. **User selects field + crop & uploads an image** from the React UI.
2. **FastAPI**:

   * Stores metadata & image reference.
   * Creates a **job record** (async mode).
3. A background worker triggers the **LangGraph pipeline**:

   * **Vision Agent** → calls Gemini Vision → returns diseases/pests/deficiencies (classification, no boxes).
   * **Weather Agent** → calls OpenMeteo → gets forecast, soil moisture, humidity, ET₀, wind, etc.
   * **Field Context Agent** → queries Chroma (RAG) with crop type + detected issues.
   * **Reasoning Agent** → synthesizes all info into a structured diagnosis.
   * **Branch in LangGraph**:

     * If severity / risk high → go to **Emergency Treatment Node**.
     * Else → go to **Standard Planner Node**.
   * **Planner Agent** → outputs a **7-day JSON plan** with recommended actions.
4. FastAPI stores the structured JSON result in SQLite.
5. User checks **Job Status** and then sees:

   * Diagnosis summary
   * Weather context
   * 7-day structured JSON plan

No PDFs, no NDVI, no satellite complexity in MVP — pure **image + weather + knowledge + agents**.

---

## 5. Core Problem the App Solves

For a given field and crop:

> “Given this crop image + upcoming weather + agronomy knowledge, what’s *really* wrong and what should we do in the coming week?”

It reduces guesswork, integrates multiple data sources, and shows how **agentic GenAI** can provide safe, explainable, structured agronomic advice — exactly in line with Syngenta’s digital + GenAI direction.

---

## 6. Expected Outcomes

* A **working, demoable, API-only, agentic AI platform** built with:

  * Gemini (LLM + Vision),
  * LangChain + LangGraph,
  * FastAPI,
  * OpenMeteo,
  * SQLite + Chroma.
* Strong interview story:

  * Multi-step reasoning,
  * Branching agent graph,
  * RAG over agronomy knowledge,
  * Multi-crop decision support.
* Clean GitHub repo you can send to Syngenta, with:

  * Docs (these three),
  * Architecture diagrams,
  * LangGraph flows,
  * Example JSON outputs.

---

## 7. Tech Stack Summary

* **LLM & Vision:** Gemini (Text + Vision APIs)
* **Backend:** FastAPI (Python)
* **Agents & Orchestration:** LangChain + LangGraph
* **Weather:** OpenMeteo API
* **Database:** SQLite (relational data)
* **Vector Store:** Chroma (embedded agronomy docs)
* **Frontend:** React + Tailwind
* **Auth (optional later):** simple JWT or mock auth for demo
* **Output format:** JSON-only (no PDFs, no email, no SMS in MVP)

---

