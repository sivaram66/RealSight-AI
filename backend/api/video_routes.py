import os
import shutil
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from backend.core.config import state, ASSETS_DIR

router = APIRouter()

@router.post("/api/upload")
async def upload_simulation_video(file: UploadFile = File(...)):
    # Save the file into the assets folder
    file_location = os.path.join(ASSETS_DIR, "custom_sim.mp4")
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Switch the global feed to the uploaded file
    state.CURRENT_STREAM_SOURCE = file_location
    return {"status": "success", "message": "Simulation feed updated."}

@router.get("/api/video")
async def serve_video():
    return FileResponse(state.CURRENT_STREAM_SOURCE)