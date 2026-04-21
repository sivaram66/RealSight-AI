from ultralytics import YOLO

class InferenceEngine:
    def __init__(self, model_path='yolov8x.pt'):
        self.model = YOLO(model_path)

    def process_frame(self, frame):
        # Strict confidence thresholds and Class 0 (Person) filtering
        results = self.model.track(frame, persist=True, verbose=False, conf=0.65, classes=[0])
        
        boxes_data = []
        frame_insights = {"person": 0, "vehicle": 0, "total_objects": 0}
        
        if results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.tolist()
            class_ids = results[0].boxes.cls.tolist()
            track_ids = results[0].boxes.id.tolist()
            
            for box, cls_id, track_id in zip(boxes, class_ids, track_ids):
                x1, y1, x2, y2 = box
                label = self.model.names[int(cls_id)]
                
                if label == "person":
                    frame_insights["person"] += 1
                elif label in ["car", "truck", "bus", "motorcycle"]:
                    frame_insights["vehicle"] += 1
                    
                frame_insights["total_objects"] += 1
                
                boxes_data.append({
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2,
                    "label": label,
                    "track_id": int(track_id)
                })
                
        return {
            "detections": boxes_data,
            "insights": frame_insights
        }

# Load the model into memory only once
engine = InferenceEngine()