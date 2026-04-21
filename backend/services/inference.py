from ultralytics import YOLO

class InferenceEngine:
    def __init__(self, model_path='yolov8s.pt'):  
        self.model = YOLO(model_path)

    def process_frame(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            verbose=False,
            conf=0.60, 
            classes=[0] # Only track persons
        )

        if not results[0].boxes or results[0].boxes.id is None:
            return {
                "detections": [],
                "insights": {"person": 0, "vehicle": 0, "total_objects": 0}
            }

        boxes_data = []
        frame_insights = {"person": 0, "vehicle": 0, "total_objects": 0}

        boxes     = results[0].boxes.xyxy.tolist()
        class_ids = results[0].boxes.cls.tolist()
        track_ids = results[0].boxes.id.tolist()
        
        frame_height = frame.shape[0]

        for box, cls_id, track_id in zip(boxes, class_ids, track_ids):
            label = self.model.names[int(cls_id)]
            
            if box[3] < (frame_height * 0.45): 
                continue 

            if label == "person":
                frame_insights["person"] += 1
                frame_insights["total_objects"] += 1
                boxes_data.append({
                    "x1": box[0], "y1": box[1], "x2": box[2], "y2": box[3],
                    "label": label,
                    "track_id": int(track_id)
                })

        return {
            "detections": boxes_data,
            "insights": frame_insights
        }

engine = InferenceEngine()