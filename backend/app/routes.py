import os
import cv2
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.services.ai_engine import EdgeInferenceService

router = APIRouter()
inference_service = EdgeInferenceService()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VIDEO_PATH = os.path.join(BASE_DIR, 'assets', 'CAM-2.mp4')

@router.websocket("/ws")
async def edge_stream_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(VIDEO_PATH)
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            payload = inference_service.process_frame(frame)
            await websocket.send_json(payload)
            await asyncio.sleep(0.04) # Roughly 25 FPS stream rate
            
    except WebSocketDisconnect:
        print("Client disconnected from stream.")
        cap.release()