import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import StatCard from '../components/StatCard';
import Uploader from '../components/Uploader';
import VideoStream from '../components/VideoStream';
import type{ WebSocketPayload, Detection, Insights } from '../types';


export default function Dashboard() {
  const [detections, setDetections] = useState<Detection[]>([]);
  const [insights, setInsights] = useState<Insights>({ person: 0, vehicle: 0, total_objects: 0 });
  const [status, setStatus] = useState<'CONNECTING' | 'SECURE' | 'OFFLINE'>('CONNECTING');
  const [videoKey, setVideoKey] = useState(0); // Changes when a new video is uploaded
  const [summary, setSummary] = useState("Initializing behavioral analysis...");

  useEffect(() => {
    // This dynamically picks the right URL based on where it's running
    setDetections([]);  
    setInsights({ person: 0, vehicle: 0, total_objects: 0 });
    const API_BASE = import.meta.env.VITE_API_URL || "localhost:8000";
    const wsUrl = window.location.protocol === "https:" 
        ? `wss://${API_BASE}/ws` 
        : `ws://${API_BASE}/ws`;

    const ws = new WebSocket(wsUrl);
    ws.onopen = () => setStatus('SECURE');
    
    ws.onmessage = (event) => {
      const data: WebSocketPayload = JSON.parse(event.data);
      if (data.summary) setSummary(data.summary);
      setDetections(data.detections);
      setInsights(data.insights);

      // const videoElement = document.querySelector('video');
      // if (videoElement && data.timestamp) {
      //   const diff = Math.abs(videoElement.currentTime - data.timestamp);
      //   // If the video is more than 0.3 seconds out of sync with the AI, snap it back
      //   if (diff > 0.3) {
      //     videoElement.currentTime = data.timestamp;
      //   }
      // }
    };

    ws.onclose = () => setStatus('OFFLINE');
    ws.onerror = () => setStatus('OFFLINE');

    return () => ws.close(); // Cleanup when user leaves page
  }, [videoKey]); // Reconnect WebSocket if videoKey changes

  const handleUploadSuccess = () => {
    // Force a reload of the Video player and WebSocket
    setVideoKey(prev => prev + 1);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '1.5rem 5%', borderBottom: '1px solid var(--border-color)', background: '#fff' }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          <div style={{ fontWeight: 700, fontSize: '1.25rem' }}>Bipolar<span style={{ color: 'var(--accent)' }}>Factory</span></div>
        </Link>
        <div style={{ fontSize: '0.875rem', fontWeight: 600, color: status === 'SECURE' ? '#10b981' : 'var(--accent)' }}>
          SYS_STATUS: {status}
        </div>
      </nav>

      {/* Upload Banner */}
      <Uploader onUploadSuccess={handleUploadSuccess} />

      {/* Main Dashboard UI */}
      <main style={{ padding: '2rem 5%', flex: 1, display: 'flex', gap: '2rem', maxWidth: '1600px', margin: '0 auto', width: '100%' }}>
        
        {/* Left Column: Video */}
        <div style={{ flex: 3 }}>
          <VideoStream detections={detections} videoKey={videoKey} />
        </div>

        {/* Right Column: Metrics */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <StatCard label="Live People Count" value={insights.person} />
          <StatCard label="Vehicles Detected" value={insights.vehicle} />
        
        </div>

      </main>
    </div>
  );
}