export const generateTelemetry = (prevState) => {
    // Simulate ship moving and data fluctuating
    const newSpeed = Math.max(0, Math.min(25, prevState.speed + (Math.random() - 0.5) * 2));
    const newHeading = (prevState.heading + (Math.random() - 0.5) * 5) % 360;
    const newLat = prevState.lat + (newSpeed * 0.001 * Math.cos((newHeading * Math.PI) / 180));
    const newLon = prevState.lon + (newSpeed * 0.001 * Math.sin((newHeading * Math.PI) / 180));
    
    // Simulate RUL decaying
    const rulDecay = Math.random() > 0.8 ? Math.random() * 50 : 0.1;
    const newRul = Math.max(0, prevState.engineRul - rulDecay);
    
    return {
        lat: newLat,
        lon: newLon,
        speed: newSpeed,
        heading: newHeading,
        engineRul: newRul,
        confidence: Math.random() > 0.95 ? 0.85 : 0.99,
        stormDist: 50 + Math.sin(Date.now() / 5000) * 20
    };
};
