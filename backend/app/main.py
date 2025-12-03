from fastapi import FastAPI 
from backend.app.routes.vision_test import router as vision_router

app = FastAPI()
app.include_router(vision_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Backend Running!"}

# if __name__ == "__main__":
    