import React, { useState, useEffect } from 'react';
import { Navigation, Wind, Cpu, Satellite } from 'lucide-react';
import { generateTelemetry } from './mockData';
import MapComponent from './components/MapComponent';

const App = () => {
  const [telemetry, setTelemetry] = useState({
    lat: 30.0, lon: -60.0, speed: 18.5, heading: 45.0, engineRul: 8500, confidence: 0.99, stormDist: 40
  });
  
  const [waypoints, setWaypoints] = useState([
    [25.0, -80.0], // Miami
    [35.0, -70.0],
    [51.5, -0.1]   // London
  ]);
  const [routePath, setRoutePath] = useState([]);

  useEffect(() => {
    // Fetch land-avoiding route when waypoints change
    const fetchRoute = async () => {
      try {
        const response = await fetch('http://localhost:5000/route', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ waypoints })
        });
        const data = await response.json();
        setRoutePath(data.path);
      } catch (e) {
        console.error("Error fetching route", e);
        setRoutePath(waypoints); // fallback
      }
    };
    fetchRoute();
  }, [waypoints]);

  const handleAddWaypoint = (latlng) => {
    setWaypoints(prev => [...prev, latlng]);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry(prev => generateTelemetry(prev));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1>Shore Operations</h1>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <span style={{ fontFamily: 'var(--font-ui)', color: 'var(--charcoal)', fontSize: '14px' }}>
            Satellite Link: ACTIVE
          </span>
          <button className="button-primary">
            <Satellite size={18} />
            Command Override
          </button>
        </div>
      </header>
      
      {/* Left Panel: Navigation Telemetry */}
      <div className="panel" style={{ gridColumn: 1 }}>
        <h2><Navigation size={24} /> Kinematics</h2>
        <p style={{ color: 'var(--body)', fontSize: '16px', marginBottom: '8px' }}>
          Real-time spatial orientation and vessel velocity derived from the Zero-Trust sensor fusion bus.
        </p>
        
        <div className="code-block">
          <div className="telemetry-item">
            <span className="telemetry-label">Speed</span>
            <span className="telemetry-value">{telemetry.speed.toFixed(1)} kn</span>
          </div>
          
          <div className="telemetry-item">
            <span className="telemetry-label">Heading</span>
            <span className="telemetry-value">{telemetry.heading.toFixed(1)}°</span>
          </div>
          
          <div className="telemetry-item">
            <span className="telemetry-label">GPS_Conf</span>
            <span className={`telemetry-value ${telemetry.confidence < 0.9 ? 'alert-amber' : ''}`}>
              {(telemetry.confidence * 100).toFixed(1)}%
            </span>
          </div>
        </div>
      </div>

      {/* Center Panel: Interactive Leaflet Map */}
      <div className="map-container">
        <MapComponent 
            shipLocation={{lat: telemetry.lat, lon: telemetry.lon}} 
            waypoints={waypoints}
            routePath={routePath}
            onAddWaypoint={handleAddWaypoint}
        />
      </div>

      {/* Right Panel: Predictive Maintenance & Weather */}
      <div className="panel" style={{ gridColumn: 3 }}>
        <h2><Cpu size={24} /> Prognostics</h2>
        <p style={{ color: 'var(--body)', fontSize: '16px', marginBottom: '8px' }}>
          PyTorch Autoencoder anomaly detection mappings.
        </p>
        
        <div className="code-block">
          <div className="telemetry-item" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%' }}>
              <span className="telemetry-label">Engine_RUL</span>
              <span className={`telemetry-value ${telemetry.engineRul < 1000 ? 'alert-red' : ''}`}>
                {Math.floor(telemetry.engineRul)}h
              </span>
            </div>
            <div className="rul-bar-container">
              <div className={`rul-bar ${telemetry.engineRul < 1000 ? 'critical' : telemetry.engineRul < 5000 ? 'warning' : ''}`} 
                   style={{ width: `${(telemetry.engineRul / 10000) * 100}%` }} />
            </div>
          </div>
        </div>

        <h2 style={{ marginTop: '24px' }}><Wind size={24} /> A* Routing</h2>
        
        <div className="code-block">
          <div className="telemetry-item">
            <span className="telemetry-label">Storm_Prox</span>
            <span className={`telemetry-value ${telemetry.stormDist < 40 ? 'alert-red' : ''}`}>
              {telemetry.stormDist.toFixed(1)} NM
            </span>
          </div>
          
          <div className="telemetry-item">
            <span className="telemetry-label">Status</span>
            <span className="telemetry-value">EVASIVE</span>
          </div>
          <p style={{ color: 'var(--on-dark)', fontSize: '12px', marginTop: '8px', borderTop: '1px solid var(--divider-dark)', paddingTop: '8px' }}>
            Click the map to drop new waypoints and override the A* algorithm.
          </p>
        </div>
      </div>
    </div>
  );
};

export default App;
