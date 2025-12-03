from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
from backend.app.services.gemini_client import get_gemini_model
from typing import Optional


VISION_AGENT_SYSTEM_PROMPT = None
with open("backend\app\prompts\vision_agent_prompt.txt", 'r', encoding="utf-8") as f:
    VISION_AGENT_SYSTEM_PROMPT = f.read()

class CropDisease(BaseModel):
    disease_detection: str = Field(description="Detected disease or deficiency in the crop")
    severity_score: int = Field(ge=0, le=100, description="Severity percentage of the crop condition")
    confidence: float = Field(ge=0, le=1, description="Model confidence in the detection (0–1)")
    possible_causes: Optional[List[str]] = Field(default=None, description="All possible causes contributing to the condition")
    recommended_actions: List[str] = Field(default_factory=list, description="Recommended actions the farmer should take")
    spray_date: Optional[str] = Field(default=None, description="Optimal spray date if relevant")
    risk_level: Optional[str] = Field(default=None, description="Risk level category (low, medium, high)")

    
model = get_gemini_model(temperature=0.1).with_structured_output(CorpDisease)

# res = model.invoke(prompt)
