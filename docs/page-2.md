
# 📄 Detailed Technical & Functional Specification

## 1. Frameworks & Libraries to Use

### Backend (FastAPI)

* `fastapi` – REST API.
* `uvicorn` – dev server.
* `pydantic` – request/response models.
* `sqlalchemy` – ORM for SQLite.
* `alembic` – DB migrations (optional).
* `httpx` or `requests` – external API calls (OpenMeteo, Gemini).
* `langchain`, `langgraph` – agents, workflows.
* `chromadb` – vector DB integration.

### Gemini Integration

* Official **Gemini Python SDK** or REST calls:

  * Text LLM for Reasoning & Planner agents.
  * Vision LLM for image analysis.

### LangChain + LangGraph

* LangChain tools/wrappers around:

  * Gemini LLM,
  * Gemini Vision,
  * Chroma retriever,
  * OpenMeteo call tool.
* LangGraph to define the **branching graph**:

  * Nodes: Vision, Weather, Context, Reason, EmergencyPlan, StandardPlan.
  * Conditional edge based on `severity_score`.

### Vector Store (Chroma)

* Store:

  * Crop profiles (per crop: Tomato, Potato, Wheat, Rice, Cotton…)
  * Common diseases & pests per crop.
  * Recommended agronomic practices (generic, not brand-specific).
* Used by:

  * Field Context Agent (RAG).
  * Optional FAQ/reasoning enhancements.

### Database (SQLite)

Tables like:

* `users` (optional)
* `fields` (name, location approx, crop_type)
* `jobs` (id, field_id, status: PENDING/RUNNING/DONE/FAILED)
* `images` (id, job_id, file_path or URL)
* `diagnoses` (job_id, JSON blob)
* `plans` (job_id, JSON blob)
* `crops` (id, name, default parameters)

### Weather (OpenMeteo)

Use OpenMeteo API to fetch:

* Temperature forecast
* Rainfall forecast
* Humidity
* Wind speed & direction (for safe spraying)
* Soil moisture (where available)
* Solar radiation
* Evapotranspiration (ET₀)

Results are stored in JSON per job and give context to reasoning and planning.

### Frontend (React + Tailwind)

* React (with Vite or CRA).
* Tailwind CSS for styling.
* `axios` or `fetch` for API calls.
* Simple routing (React Router optional).

No infra/monitoring stack needed in docs per your constraint.

---

## 2. Roles & Functionalities

Even though you may not implement full auth at first, define roles as part of the spec for maturity.

### Role: Farmer / Field User

* Create & select fields (with approximate location, crop type).
* Upload crop photos.
* Trigger analysis for a field.
* View:

  * Job status (PENDING/RUNNING/DONE/FAILED).
  * Diagnosis JSON summary (rendered nicely).
  * 7-day plan in table format.

### Role: Agronomist

* View all fields & jobs.
* See underlying JSON reasoning outputs.
* Override plan or annotate with feedback (stored in DB).
* Mark cases as “validated” vs “needs review”.

### Role: Admin (optional)

* Manage crop list (predefined crops).
* Manage knowledge base documents for Chroma.
* View statistics (number of jobs, average severity, etc.).

For MVP, you can keep this conceptual and just implement one “default user” while still mentioning roles in docs.

---

## 3. Key Terminologies

* **Multi-crop System:** The app supports multiple crops (e.g., Tomato, Potato, Wheat, Rice, Cotton), each with its own typical diseases, pests, and agronomic rules.
* **Agent:** A specialized component (often backed by an LLM or API) responsible for a specific task (vision, weather, reasoning…).
* **Agentic Workflow:** A coordinated sequence/graph of agents (via LangGraph) with conditional flows.
* **Vision Agent:** Uses Gemini Vision to classify crop issues from the image.
* **Weather Agent:** Queries OpenMeteo for short-term forecasts and agro-meteorological indicators.
* **Field Context Agent:** Uses Chroma vector store to retrieve relevant agronomy knowledge.
* **Reasoning Agent:** Uses Gemini text LLM to synthesize all inputs into a detailed diagnosis.
* **Planner Agent:** Uses Gemini to turn diagnosis into a structured 7-day plan, with branching logic.
* **Severity Score:** A scalar (0–1 or 0–100) representing how critical the detected issue is.

---

## 4. Similar Apps (Comparison)

1. **Plantix**

   * Image-based disease detection, farmer UI, multi-crop.
   * Limited explicit multi-agent reasoning; more CV-risk focus.

2. **Taranis**

   * Aerial imagery, advanced CV, scouting reports.
   * More enterprise, less open agentic LLM.

3. **Cropwise (Syngenta)**

   * Complete digital farming platform with decision support.
   * Your project mirrors its **digital advisory + AI reasoning**, but in a simplified research/academic form with open APIs.

4. **AgroScout**

   * Drone-based scouting and detection.
   * Less emphasis on RAG + LLM planning.

**Differentiation:**
AgroAgentX is **explicitly built as an agentic, API-driven, Gemini-based multi-crop decision system** with a branching LangGraph pipeline and structured JSON outputs.

---

## 5. Application Wireframe (Text-Based)

### Screen 1 — Login / Home (simple)

* If you skip auth, this just shows a **“Go to Dashboard”** button.

### Screen 2 — Dashboard

* **Header:** “AgroAgentX”
* Cards:

  * “Fields Monitored”
  * “Jobs Running”
  * “Jobs Completed”
* Button: **“Create New Field”**
* Table: recent jobs (Field, Crop, Status, Created at, View Results)

### Screen 3 — Create / Select Field

* Form fields:

  * Field Name
  * Crop Type (dropdown: Tomato/Potato/Wheat/Rice/Cotton)
  * Approx Location (optional text)
* Button: **Save Field**
* List of existing fields with **“Analyze Field”** button.

### Screen 4 — Analyze Field (Upload UI)

* Shows selected field metadata.
* File upload: **Select Image**
* Button: **Run Analysis**
* On submit: shows “Job ID” and “Status: PENDING” and polls status.

### Screen 5 — Job Detail / Result

* Section: Job Info (Field, Crop, Status, Created at).
* Section: Diagnosis Summary (rendered from JSON)

  * Top 3 detected issues with severity.
  * Weather summary (rain, temp, ET₀, wind for spraying).
* Section: Plan (7-day plan in table form)

  * Day, Action, Notes, Safety flags.
* Section: Raw JSON viewer (collapsible).

### Screen 6 — Admin / Knowledge Base (optional)

* List of knowledge docs.
* Button to add/edit crop-specific disease docs.

---

## 6. Core Features

* **Field & Crop Management** (multi-crop-predefined).
* **Async Job-based Analysis**:

  * Job record with status (PENDING/RUNNING/DONE/FAILED).
* **Gemini Vision-based Issue Classification**:

  * No bounding boxes, but robust textual + structured classification.
* **OpenMeteo Weather Context** for every job.
* **Chroma-backed Context Retrieval** (RAG).
* **Branching LangGraph Workflow**:

  * Standard vs Emergency treatment paths based on severity.
* **JSON-Only Structured Outputs**:

  * Diagnosis JSON
  * Plan JSON
* **React + Tailwind UI** for:

  * Upload
  * Result visualization
  * Viewing JSON in a friendly way.

---

## 7. Recommended / Optional Features

* Agronomist review & correction logging.
* Feedback loop where agronomist corrections are stored and used as:

  * Additional RAG documents.
  * Prompt examples for better planning.
* Minimal authentication with JWT + role tags.
* A small “What-if” simulator:

  * Change the weather scenario and recompute plan.
* History analytics:

  * Which crop sees most severe alerts?
  * Which actions are suggested most often?

---