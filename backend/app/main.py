from fastapi import FastAPI 
from backend.app.routes.vision_test import router as vision_router
from backend.app.routes.vision_crop import router as crop_router
from backend.app.routes.weather import router as weather_router


app = FastAPI()
app.include_router(vision_router, prefix="/api")
app.include_router(crop_router, prefix="/api")
app.include_router(weather_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend Running!"}

# if __name__ == "__main__":
    