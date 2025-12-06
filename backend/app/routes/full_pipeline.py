from fastapi import APIRouter, UploadFile, HTTPException
from fastapi import status
import httpx
from base64 import b64encode

router = APIRouter()

@router.post("/full-analysis")
async def full_analysis(image: UploadFile):
    try:
        # 1) Read image for reuse
        image_bytes = await image.read()

        # ------------------------------------
        # 2) CALL VISION AGENT (internal API)
        # ------------------------------------
        async with httpx.AsyncClient() as client:
            vis_res = await client.post(
                "http://localhost:8000/api/vision-crop",
                files={"image": ("image.png", image_bytes, "image/png")}
            )
        crop_disease = vis_res.json().get("response")

        # ------------------------------------
        # 3) CALL WEATHER API
        # ------------------------------------
        async with httpx.AsyncClient() as client:
            w_res = await client.get("http://localhost:8000/api/weather")
        weather = w_res.json().get("weather", {}).get("current", {})

        # ------------------------------------
        # 4) CALL AGRONOMY AGENT
        # ------------------------------------
        async with httpx.AsyncClient() as client:
            ag_res = await client.post(
                "http://localhost:8000/api/agronomy",
                json={
                    "crop_disease": crop_disease,
                    "weather": weather
                }
            )
        agronomy = ag_res.json().get("response")

        # ------------------------------------
        # 5) CALL RECOMMENDATION AGENT
        # ------------------------------------
        async with httpx.AsyncClient() as client:
            rec_res = await client.post(
                "http://localhost:8000/api/recommendation",
                json={
                    "crop_disease": crop_disease,
                    "agronomy_advice": agronomy
                }
            )
        recommendation = rec_res.json().get("response")

        # ------------------------------------
        # 6) FINAL RESPONSE
        # ------------------------------------
        return {
            "crop_disease": crop_disease,
            "weather": weather,
            "agronomy": agronomy,
            "recommendation": recommendation
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
