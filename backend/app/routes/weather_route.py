from fastapi import APIRouter
from backend.app.services.weather_simple import get_static_weather

router = APIRouter()

@router.get("/weather")
async def weather():
    data = await get_static_weather()
    return {"weather": data}