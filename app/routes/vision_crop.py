from fastapi import APIRouter, UploadFile
# from backend.app.services.gemini_client import get_gemini_model
from backend.app.agents.vision_agent import VISION_AGENT_SYSTEM_PROMPT, vision_agent
from base64 import b64encode
from langchain_core.messages import HumanMessage, SystemMessage

router = APIRouter()

@router.post("/vision-crop")
async def vision_crop(image: UploadFile):
    image_bytes = await image.read()
    img_b64 = b64encode(image_bytes).decode("utf-8")
    
    human_msg = HumanMessage(
        content = [
            {
                "type": "image",
                "base64": img_b64,
                "mime_type": "image/png"
            }
        ]
    )
    system_message = SystemMessage(content = VISION_AGENT_SYSTEM_PROMPT)
    res = vision_agent.invoke([system_message, human_msg])
    
    return {"response": getattr(res, "content", None) or getattr(res, "content_blocks", res)}