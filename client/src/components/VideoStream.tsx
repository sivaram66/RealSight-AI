import { useEffect, useRef } from 'react';
import type { Detection } from '../types';

interface VideoStreamProps {
  detections: Detection[];
  videoKey: number; // A trick to force the video to reload when a new file is uploaded
}

export default function VideoStream({ detections, videoKey }: VideoStreamProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const videoRef = useRef<HTMLVideoElement>(null);

  // Draw the red boxes whenever the WebSocket sends new detections
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear the previous frame's drawings
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    detections.forEach(det => {
      // Draw Box
      ctx.beginPath();
      ctx.strokeStyle = '#ff3366'; // Bipolar Red
      ctx.lineWidth = 3;
      ctx.rect(det.x1, det.y1, det.x2 - det.x1, det.y2 - det.y1);
      ctx.stroke();

      // Draw Label Background
      ctx.fillStyle = '#ff3366';
      ctx.fillRect(det.x1, det.y1 - 25, 100, 25);

      // Draw Label Text
      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 12px Inter';
      ctx.fillText(`${det.label.toUpperCase()} ${det.track_id}`, det.x1 + 5, det.y1 - 7);
    });
  }, [detections]);

  return (
    <div style={{ position: 'relative', width: '100%', overflow: 'hidden', background: '#000', borderRadius: '8px' }}>
      <video 
        key={videoKey} ref={videoRef}
        src={`http://localhost:8000/api/video?t=${videoKey}`}
        autoPlay loop muted playsInline
        style={{ width: '100%', display: 'block' }}
        onLoadedMetadata={() => {
          // Sync canvas resolution to the exact video file resolution
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