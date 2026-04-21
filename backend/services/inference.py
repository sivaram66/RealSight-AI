from ultralytics import YOLO

class InferenceEngine:
    # 1. WE MUST USE THE SMALL MODEL. The 'X' model is causing the video lag/ghosting!
    def __init__(self, model_path='yolov8s.pt'):  
        self.model = YOLO(model_path)

    def process_frame(self, frame):
        # 2. Let the AI do the heavy lifting. No custom trackers, just a clean 60% confidence.
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
            
            # 3. ONLY ONE FILTER: The Maybelline Poster Filter.
            # If the bottom of the box doesn't reach the bottom 55% of the screen, it's a poster.
            # We removed the aspect ratio and size filters so the backpack girl isn't hidden!
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