import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.api.routes import router

app = FastAPI(title="RealSight AI", description="Edge Inference Telemetry Platform")

app.include_router(router)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="assets")

@app.get("/")
async def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, 'index.html'))