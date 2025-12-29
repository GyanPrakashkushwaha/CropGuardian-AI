from pydantic import BaseModel, Field
from backend.app.services.gemini_client import get_gemini_model


class AgronomyAdvice(BaseModel):
    risk_level: str = Field(description="low, medium, or high disease risk OR 'uncertain diagnosis'")
    spray_window: str = Field(description="safe or unsafe spray window based on weather conditions")
    urgency: str = Field(description="low, medium, or high urgency based on disease severity")
    advice: str = Field(description="Farmer-friendly final advice combining disease and weather info")

AGRONOMY_AGENT_SYSTEM_PROMPT = None
with open(r"backend\app\prompts\agronomy_agent_prompt.txt", 'r', encoding="utf-8") as f:
    AGRONOMY_AGENT_SYSTEM_PROMPT = f.read()

agronomy_agent = get_gemini_model(temperature=0.1).with_structured_output(AgronomyAdvice)
