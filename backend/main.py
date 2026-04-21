import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load the variables from .env
load_dotenv()

# 2. CREATE THE APP INSTANCE FIRST
app = FastAPI(title="RealSight Edge AI API")

# 3. Import your routers AFTER creating the app (best practice)
from backend.api.video_routes import router as video_router
from backend.api.ws_routes import router as ws_router

# 4. Now you can use 'app' to add middleware
frontend_url = os.getenv("FRONTEND_URL")
allowed_origins = [frontend_url] if frontend_url else ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Health Check
@app.get("/health")
async def health_check():
    return {"status": "online"}

# 6. Include Routers
app.include_router(video_router)
app.include_router(ws_router)