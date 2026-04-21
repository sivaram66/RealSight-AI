// A single bounding box detection
export interface Detection {
    x1: number;
    y1: number;
    x2: number;
    y2: number;
    label: string;
    track_id: number;
}

// The analytics for the current frame
export interface Insights {
    person: number;
    vehicle: number;
    total_objects: number;
}

// The complete JSON payload sent from the FastAPI WebSocket
export interface WebSocketPayload {
    detections: Detection[];
    insights: Insights;
    summary?: string;
    timestamp?: number;
}