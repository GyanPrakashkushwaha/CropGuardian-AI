### High-Level Architecture Diagram
```
                      ┌────────────────────────────┐
                      │         Frontend            │
                      │     React + Tailwind        │
                      └─────────────┬──────────────┘
                                    │ HTTP (REST)
                                    ▼
                      ┌────────────────────────────┐
                      │          FastAPI            │
                      │ (Job creation, status, I/O) │
                      └─────────────┬──────────────┘
                                    │ triggers
                                    ▼
                      ┌────────────────────────────┐
                      │        LangGraph Engine     │
                      │  (Branching Agent Workflow) │
                      └─────────────┬──────────────┘
        ┌───────────────────────────┼──────────────────────────────┐
        ▼                           ▼                              ▼
┌─────────────────┐      ┌──────────────────────┐       ┌───────────────────────┐
│   Vision Agent   │      │    Weather Agent     │       │ Field Context Agent   │
│ Gemini Vision API│      │   OpenMeteo APIs     │       │ Chroma RAG Retrieval  │
└─────────────────┘      └──────────────────────┘       └───────────────────────┘
        │                           │                              │
        └───────────────┬───────────┴─────────────┬───────────────┘
                        ▼                         ▼
              ┌────────────────────┐   ┌───────────────────────┐
              │   Reasoning Agent  │   │ Branching Logic Node  │
              │ (Gemini Text LLM)  │   │ severity_score check  │
              └───────────┬────────┘   └───────────┬──────────┘
                          │                        │
                          ▼                        ▼
            ┌────────────────────┐    ┌────────────────────────┐
            │ Standard Planner   │    │ Emergency Planner       │
            │ (Gemini Text LLM)  │    │ (altered prompt path)   │
            └───────────┬────────┘    └───────────┬────────────┘
                        │                         │
                        └─────────┬───────────────┘
                                  ▼
                          ┌─────────────────┐
                          │    SQLite DB    │
                          │ Fields, Jobs,   │
                          │ Diagnoses, Plan │
                          └─────────────────┘
```


### End-to-End Workflow Diagram
```
[User Uploads Image]
          │
          ▼
┌──────────────────────┐
│ FastAPI: Create Job  │
│ Save image + metadata│
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ Background Worker    │
│ triggers LangGraph   │
└──────────┬───────────┘
           
           ▼
   ┌──────────────────┐
   │  Vision Agent     │
   │ Gemini Vision API │
   └─────────┬────────┘
             │
             ▼
   ┌──────────────────┐
   │ Weather Agent     │
   │ Calls OpenMeteo   │
   └─────────┬────────┘
             │
             ▼
   ┌──────────────────┐
   │ Field Context     │
   │ Chroma RAG        │
   └─────────┬────────┘
             │
             ▼
   ┌──────────────────┐
   │ Reasoning Agent   │
   │ Synthesizes info  │
   └─────────┬────────┘
             │
             ▼
    ┌─────────────────┐
    │ severity_score? │
    └────────┬────────┘
             │
        ┌────┴──────┐
        │           │
        ▼           ▼
┌────────────┐   ┌────────────────┐
│ Standard   │   │ Emergency Plan │
│ Planner    │   │ Planner Agent  │
└──────┬─────┘   └───────┬────────┘
        │                 │
        └──────┬──────────┘
               ▼
    ┌────────────────────────┐
    │ Save JSON to SQLite    │
    │ (diagnosis + plan)     │
    └───────────┬────────────┘
                │
                ▼
     [Frontend fetches results]
```

### Component Relationship Diagram
```
                    ┌───────────────┐
                    │ React Frontend │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    FastAPI     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   LangGraph    │
                    └───────┬───────┘
        ┌───────────┬───────┼─────────────┬───────────┐
        ▼           ▼       ▼             ▼           ▼
┌────────────┐┌───────────┐┌────────────┐┌──────────┐┌──────────────┐
│ Vision     ││ Weather    ││ Context    ││ Reason   ││ Planner      │
│ (Gemini)   ││ (OpenMeteo)││ (Chroma)   ││ (LLM)    ││ (LLM)        │
└────────────┘└───────────┘└────────────┘└──────────┘└──────────────┘
                            │
                            ▼
                      ┌──────────────┐
                      │   SQLite DB   │
                      └──────────────┘
```