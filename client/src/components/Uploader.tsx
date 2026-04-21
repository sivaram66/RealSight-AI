import { useState } from 'react';

// 1. We grab the dynamic URL from Vercel's environment variables
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Uploader({ onUploadSuccess }: { onUploadSuccess: () => void }) {
  const [isUploading, setIsUploading] = useState(false);
  
  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      // 2. We use the dynamic API_BASE instead of the hardcoded localhost
      const res = await fetch(`${API_BASE}/api/upload`, {
        method: 'POST',
        body: formData
      });
      if (res.ok) {
        onUploadSuccess(); // Tells the dashboard to reload the video
      } else {
        alert("Upload failed. Ensure backend is running.");
      }
    } catch (err) {
      console.error(err);
      alert("Server error during upload.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div style={{ 
      display: 'flex', alignItems: 'center', gap: '1rem', padding: '1rem', 
      background: 'var(--surface-color)', borderBottom: '1px solid var(--border-color)' 
    }}>
      <div style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
        <strong>SIMULATION MODULE:</strong> Upload MP4 to override CCTV feed.
      </div>
      <input 
        type="file" accept="video/mp4" 
        onChange={handleFileChange} disabled={isUploading}
        style={{ fontSize: '0.875rem' }}
      />
      {isUploading && <span style={{ fontSize: '0.875rem', color: 'var(--accent)', fontWeight: 'bold' }}>Injecting...</span>}
    </div>
  );
}