from fastapi import FastAPI 
from backend.app.routes.vision_test import router as vision_router
from backend.app.routes.vision_crop import router as crop_router
from backend.app.routes.weather_route import router as weather_router
from backend.app.routes.agronomy_route import router as agronomy_router
from backend.app.routes.recommendation_route import router as recommendation_route
from backend.app.routes.full_pipeline import router as full_analysis_router

app = FastAPI()
# app.include_router(vision_router, prefix="/api")
app.include_router(crop_router, prefix="/api")
app.include_router(weather_router, prefix="/api")
app.include_router(agronomy_router, prefix="/api")
app.include_router(recommendation_route, prefix="/api")
app.include_router(full_analysis_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend Running!"}

# if __name__ == "__main__":
    