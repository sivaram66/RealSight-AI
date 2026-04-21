from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import our modular routers
from backend.api.video_routes import router as video_router
from backend.api.ws_routes import router as ws_router

app = FastAPI(title="RealSight Edge AI API")

# Allow Vite to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW DEVOPS HEALTH CHECK ROUTE ---
@app.get("/health")
async def health_check():
    return {
        "status": "online",
        "service": "RealSight Edge AI API",
        "version": "1.0.0",
        "pipeline": "secure"
    }

# Mount the application routers
app.include_router(video_router)
app.include_router(ws_router)