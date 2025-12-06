from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.agents.recommendation_agent import RECOMMENDATION_AGENT_SYSTEM_PROMPT, recommendation_agent
from langchain_core.messages import HumanMessage, SystemMessage
import json

router = APIRouter()

class RecommendationRequest(BaseModel):
    crop_disease: dict
    agronomy_advice: dict
    
@router.post("/recommendation")
async def recommendation_handler(req: RecommendationRequest):
    crop_disease_json = json.dumps(req.crop_disease)
    agronomy_advice_json = json.dumps(req.agronomy_advice)
    
    system_message = SystemMessage(content=RECOMMENDATION_AGENT_SYSTEM_PROMPT)
    human_msg = HumanMessage(
        content=[
            {"type": "text", "text": "Please review the data and give recommendations."},
            {"type": "text", "text": crop_disease_json},
            {"type": "text", "text": agronomy_advice_json},
        ]
    )
    try:
        res = recommendation_agent.invoke([system_message, human_msg]) 
    except TypeError:
        res = await recommendation_agent.invoke({"messages": [human_msg]})

    return {"response": getattr(res, "content", None) or getattr(res, "content_blocks", res)}
