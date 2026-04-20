from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import asyncio
from ultralytics import YOLO

app = FastAPI()

# 1. Load the model once when the server starts
model = YOLO('yolov8n.pt')

# 2. Open the WebSocket tunnel
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture('CAM-2.mp4')
    
    try:
        while True:
            success, frame = cap.read()
            
            # If the video ends, seamlessly loop it back to the beginning
            if not success:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
                
            # Run inference (verbose=False keeps terminal clean)
            results = model(frame, verbose=False)
            payload = []
            
            # Extract coordinates and labels for every object found
            for box in results[0].boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_id = int(box.cls[0].item())
                label = model.names[class_id] # Gets the text name, like "person"
                
                payload.append({
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "label": label
                })
                
            # Blast the JSON data through the tunnel to the frontend
            await websocket.send_json(payload)
            
            # Crucial: Throttle the loop slightly so we don't crash the browser
            await asyncio.sleep(0.05)
            
    except WebSocketDisconnect:
        print("Client disconnected.")
        cap.release()