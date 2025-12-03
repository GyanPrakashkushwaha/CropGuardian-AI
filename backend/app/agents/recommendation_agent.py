from backend.app.services.gemini_client import get_gemini_model
from pydantic import BaseModel, Field
from typing import List

class RecommendationPlan(BaseModel):
    summary: str = Field(description="Overall summary of the situation")
    today_actions: List[str] = Field(description="Specific tasks to perform today")
    next_3_days: List[str] = Field(description="Actions for the next 1–3 days")
    monitoring_tips: List[str] = Field(description="What the farmer should monitor daily")
    warnings: List[str] = Field(description="Potential risks based on disease and weather")

RECOMMENDATION_AGENT_SYSTEM_PROMPT = None
with open(r"backend\app\prompts\recommendation_agent_prompt.txt", 'r', encoding="utf-8") as f:
    RECOMMENDATION_AGENT_SYSTEM_PROMPT = f.read()
    
recommendation_agent = get_gemini_model().with_structured_output(RecommendationPlan)