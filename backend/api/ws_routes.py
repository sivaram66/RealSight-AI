import cv2
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.core.config import state
from backend.services.inference import engine

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    cap = cv2.VideoCapture(state.CURRENT_STREAM_SOURCE) 
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            payload = engine.process_frame(frame)
            await websocket.send_json(payload)
            await asyncio.sleep(0.04) 
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        cap.release()