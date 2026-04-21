import { Link } from 'react-router-dom';

export default function Landing() {
  return (
    <div className="landing-container">
      <nav className="navbar">
        <div className="logo">
          Bipolar<span>Factory</span>
        </div>
        <div className="nav-badge">AI Engineer Assignment</div>
      </nav>

      <main className="hero">
        <div className="hero-content">
          <h1>Intelligence at the <span>Edge.</span></h1>
          <p>
            A zero-latency, WebSocket-driven inference pipeline simulating 
            production-grade retail analytics. Built completely from scratch. 
          </p>
          
          <div className="cta-container">
            <Link to="/dashboard" className="cta-button">
              Launch Dashboard &rarr;
            </Link>
          </div>
        </div>
      </main>

      <footer className="footer">
        <p>Engineered for secure edge deployment.</p>
      </footer>
    </div>
  );
}