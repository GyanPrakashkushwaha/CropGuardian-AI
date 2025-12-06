from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.agents.agronomy_agent import AGRONOMY_AGENT_SYSTEM_PROMPT, agronomy_agent
from langchain_core.messages import HumanMessage, SystemMessage
import json

router = APIRouter()

class AgronomyRequest(BaseModel):
    crop_disease: dict
    weather: dict

@router.post("/agronomy")
async def agronomy_handler(req: AgronomyRequest):
    crop_disease_json = json.dumps(req.crop_disease)
    weather_json = json.dumps(req.weather)
    
    system_message = SystemMessage(content=AGRONOMY_AGENT_SYSTEM_PROMPT)
    human_msg = HumanMessage(
        content=[
            {"type": "text", "text": crop_disease_json},              # send JSON as text block
            {"type": "text", "text": weather_json},
        ]
    )
    try:
        res = agronomy_agent.invoke([system_message, human_msg])  # synchronous invoke
    except TypeError:
        # 2) If agronomy_agent is an agent (LangGraph/agent), pass a dict with messages and await
        res = await agronomy_agent.invoke({"messages": [human_msg]})

    # Response object shapes vary by provider / wrapper; inspect `res` for content or content_blocks
    return {"response": getattr(res, "content", None) or getattr(res, "content_blocks", res)}
