import { useEffect, useRef } from 'react';
import type { Detection } from '../types';

interface VideoStreamProps {
  detections: Detection[];
  videoKey: number;
}

export default function VideoStream({ detections, videoKey }: VideoStreamProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  // Dynamic URL logic: uses .env variable if it exists, otherwise defaults to local
  const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

  useEffect(() => {
  const canvas = canvasRef.current;
  const video = videoRef.current;
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  // ✅ Always sync canvas resolution to video before clearing
  if (video && video.videoWidth > 0) {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
  }

  // Now clear reliably works
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  if (!detections || detections.length === 0) return;

  detections.forEach(det => {
    ctx.beginPath();
    ctx.strokeStyle = '#ff3366';
    ctx.lineWidth = 3;
    ctx.rect(det.x1, det.y1, det.x2 - det.x1, det.y2 - det.y1);
    ctx.stroke();
    ctx.fillStyle = '#ff3366';
    ctx.fillRect(det.x1, det.y1 - 25, 90, 25);
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px Inter';
    ctx.fillText(`PERSON ${det.track_id}`, det.x1 + 5, det.y1 - 7);
  });
}, [detections]);
  return (
    <div style={{ position: 'relative', width: '100%', overflow: 'hidden', background: '#000', borderRadius: '8px' }}>
      <video 
        key={videoKey} 
        ref={videoRef}
        // Uses the dynamic cloud or local URL
        src={`${API_BASE}/api/video?t=${videoKey}`}
        autoPlay loop muted playsInline
        style={{ width: '100%', display: 'block' }}
        onLoadedMetadata={() => {
          if (canvasRef.current && videoRef.current) {
            canvasRef.current.width = videoRef.current.videoWidth;
            canvasRef.current.height = videoRef.current.videoHeight;
          }
        }}
      />
      <canvas 
        ref={canvasRef}
        style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}
      />
    </div>
  );
}