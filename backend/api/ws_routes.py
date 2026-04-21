import cv2
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.core.config import state
from backend.services.inference import engine
from backend.services.llm import analyze_behavior # Import the new service

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(state.CURRENT_STREAM_SOURCE) 
    frame_counter = 0
    
    # Background task handler
    async def update_summary(frame_to_analyze):
        new_summary = await analyze_behavior(frame_to_analyze)
        state.CURRENT_SUMMARY = new_summary
    
    try:
        while True:
            success, frame = cap.read()
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            frame_counter += 1
            
            # Every ~6 seconds, grab a copy of the frame and send it to Groq asynchronously
            if frame_counter % 150 == 0:
                asyncio.create_task(update_summary(frame.copy()))
                
            payload = engine.process_frame(frame)
            
            # Inject the current LLM summary into the WebSocket JSON
            payload["summary"] = state.CURRENT_SUMMARY 
            
            await websocket.send_json(payload)
            await asyncio.sleep(0.04) 
            
    except WebSocketDisconnect:
        print("Client disconnected.")
    finally:
        cap.release()