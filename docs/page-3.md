
# 📄 Project Roadmap & Milestones

Time estimates assume **one person** working focused; adjust based on your schedule.

Progress bars are conceptual (how far you are from completion of that milestone).

---

## Milestone 0 — Planning, Setup & Knowledge Base

**Description:**
Set up project skeleton, create initial agronomy knowledge base for Chroma, and define schemas & prompts.

**Tasks:**

* Initialize Git repo, basic folder structure (backend, frontend, docs).
* Install FastAPI, LangChain, LangGraph, Chroma, Gemini SDK.
* Design DB schema (SQLite) for fields, jobs, diagnoses, plans.
* Define JSON schemas for diagnosis & plan.
* Prepare initial knowledge documents:

  * Per-crop typical diseases/pests.
  * Generic best-practice treatments.
* Seed Chroma with these docs.

**Expected Time:** 1–3 days (8–20 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 1 — Backend Skeleton & Job System (Async)

**Description:**
Create FastAPI basics, SQLite integration, job model, and a simple async pattern (status polling).

**Tasks:**

* FastAPI setup with `/fields`, `/jobs` endpoints.
* SQLite integration + SQLAlchemy models:

  * Field
  * Job
* Job states: PENDING, RUNNING, DONE, FAILED.
* A simple background worker:

  * Could be a FastAPI background task.
  * Or a simple internal scheduler.
* Endpoint to:

  * Create job (when user uploads image).
  * Get job status and result.

**Expected Time:** 2–3 days (12–20 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 2 — Vision Agent (Gemini Vision) Integration

**Description:**
Plug Gemini Vision into your pipeline as the Vision Agent and produce structured classification from images.

**Tasks:**

* Write a LangChain Tool/Wrapper that calls Gemini Vision with image.

* Define fixed prompt to produce structured output, e.g.:

  ```json
  {
    "crop": "...",
    "possible_diseases": [...],
    "possible_pests": [...],
    "nutrient_deficiencies": [...],
    "severity_score": 0.0
  }
  ```

* Integrate this Tool as **Vision Node** in LangGraph.

* Update job processing to:

  * Read image path/bytes.
  * Call Vision Agent.
  * Store Vision output in DB as JSON.

**Expected Time:** 3–4 days (15–25 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 3 — Weather Agent (OpenMeteo) & Context Agent (Chroma RAG)

**Description:**
Add the Weather Agent and Field Context Agent nodes to the graph.

**Tasks:**

* Implement OpenMeteo client function:

  * Given location (lat/lon or region approx), fetch:

    * Temp forecast
    * Rainfall
    * Humidity
    * Wind
    * Soil moisture
    * Solar radiation
    * ET₀
* Wrap it as a LangChain Tool.
* Implement Chroma retriever:

  * Query docs based on crop, detected diseases, severity.
* Build **Field Context Agent** node in LangGraph:

  * Input: crop type + detections.
  * Output: aggregated context text/snippets.
* Ensure both outputs are stored and passed along as structured inputs.

**Expected Time:** 3–5 days (18–30 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 4 — Reasoning & Planner Agents with Branching LangGraph

**Description:**
Complete the agentic pipeline with reasoning and planning, including **branching logic** for severity.

**Tasks:**

* Reasoning Agent:

  * Use Gemini text LLM.
  * Input = Vision output + Weather output + Context snippets.
  * Output structured diagnosis JSON (clear, machine-friendly).
* Planner Agent:

  * Use Gemini text LLM.
  * Take diagnosis JSON.
  * Output 7-day plan JSON.
* Implement **branching in LangGraph**:

  * Node that checks `severity_score`.
  * If above threshold → route to EmergencyPlanNode.
  * Else → StandardPlanNode (both using Planner Agent with slightly different prompt templates).
* Wire LangGraph into main job executor in FastAPI.
* Save `diagnosis` + `plan` JSON into SQLite.

**Expected Time:** 1–1.5 weeks (30–50 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 5 — React + Tailwind Frontend

**Description:**
Build a clean, professional UI for fields, jobs and results viewing.

**Tasks:**

* Set up React + Tailwind project.
* Screens:

  * Dashboard list of fields and jobs.
  * Create Field form (with multi-crop dropdown).
  * Analyze Field screen (image upload → create job).
  * Job Detail screen:

    * Show status.
    * Show diagnosis summary (JSON → cards/table).
    * Show 7-day plan nicely formatted.
    * Show raw JSON viewer.
* Add polling for job status.
* Handle loading/error states.

**Expected Time:** 1 week (25–40 hours)
**Progress:** 📊 0% → 100%

---

## Milestone 6 — Polish, Multi-Crop Enhancements & Interview Packaging

**Description:**
Make it impressive, robust and ready to demo to Syngenta.

**Tasks:**

* Improve multi-crop prompting:

  * Adjust prompts depending on selected crop.
* Tune severity thresholds for branching.
* Add small “Sample Data Mode”:

  * Pre-defined demo jobs for offline demo.
* Write:

  * README with diagrams.
  * Short “System Design for Syngenta” doc.
* Create short demo video (screen recording) walking through:

  * Field selection → upload → job → diagnosis → plan.

**Expected Time:** 1 week (20–30 hours)
**Progress:** 📊 0% → 100%

---

## 🔚 Project Completion Overview

* **Total Estimated Time (Single Dev, Strong MVP):**
  ~6–8 weeks (120–200 focused hours), depending on how polished you want it.

* **Phases & Dependencies:**

  * Milestone 0 → baseline setup, knowledge, schemas.
  * Milestone 1 → job infra (critical for async).
  * Milestone 2–4 → core multi-agent AI logic (heart of the system).
  * Milestone 5 → user-facing UI.
  * Milestone 6 → polish + interview packaging.

* **Critical Path:**

  * Gemini & OpenMeteo API access working.
  * LangGraph pipeline successfully wired into FastAPI.
  * JSON schema consistency between agents.
  * Multi-crop support stable in prompts & UI.

---

