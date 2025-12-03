from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()
from backend.app.services.gemini_client import get_gemini_model
from typing import Optional
from typing import List

VISION_AGENT_SYSTEM_PROMPT = None
with open(r"backend\app\prompts\vision_agent_prompt.txt", 'r', encoding="utf-8") as f:
    VISION_AGENT_SYSTEM_PROMPT = f.read()

class CropDisease(BaseModel):
    disease_detection: str = Field(description="Detected disease or deficiency in the crop")
    severity_score: int = Field(ge=0, le=100, description="Severity percentage of the crop condition")
    confidence: float = Field(ge=0, le=1, description="Model confidence in the detection (0–1)")
    possible_causes: Optional[List[str]] = Field(default=None, description="Visual-only possible causes of the condition")
    recommended_actions: List[str] = Field(default_factory=list, description="Actionable steps a farmer should take immediately (WITHOUT chemicals)")


    
model = get_gemini_model(temperature=0.1).with_structured_output(CropDisease)

# res = model.invoke(prompt)
