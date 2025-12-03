from fastapi import APIRouter, UploadFile
from backend.app.services.gemini_client import get_gemini_model
from base64 import b64encode
from langchain_core.messages import HumanMessage

router = APIRouter()

@router.post("/vision-test")
async def vision_test(image: UploadFile):
    model = get_gemini_model()
    image_bytes = await image.read()
    img_b64 = b64encode(image_bytes).decode("utf-8")
    
    human_msg = HumanMessage(
        content = [
            {
                "type": "text", 
                "text": "Describe this crop image."
            },
            {
                "type": "image",
                "base64": img_b64,
                "mime_type": "image/png"
            }
        ]
    )
    
    res = model.invoke([human_msg])
    
    return {"response": getattr(res, "content", None) or getattr(res, "content_blocks", res)}