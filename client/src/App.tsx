import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import './styles/globals.css';

function App() {
  return (
    <Router>
      <Routes>
        {/* Step 1: The bold marketing page */}
        <Route path="/" element={<Landing />} />
        
        {/* Step 2: The live YOLOv8 inference dashboard */}
        <Route path="/dashboard" element={<Dashboard />} />
        
        {/* Catch-all: Redirect unknown URLs back to the start */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;