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
    
    frame_counter = 0
    frame_skip = 3  # Keeps the AI perfectly in sync with React video
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            frame_counter += 1
            
            # Frame Skipping Engine
            if frame_counter % frame_skip != 0:
                await asyncio.sleep(0.001)
                continue
                
            # Process frame with YOLOv8
            payload = engine.process_frame(frame)

            # Add timestamp for sync
            current_time_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            payload["timestamp"] = current_time_sec
            
            await websocket.send_json(payload)
            await asyncio.sleep(0.01) 
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        cap.release()