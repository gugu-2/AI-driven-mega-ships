import React from 'react';
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents, LayersControl, LayerGroup } from 'react-leaflet';
import L from 'leaflet';

// Fix for default marker icons in React Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom ship icon (orange dot)
const shipIcon = L.divIcon({
  className: 'custom-ship-icon',
  html: '<div class="ship-marker-inner"></div>',
  iconSize: [24, 24],
  iconAnchor: [12, 12]
});

// Component to handle map clicks for adding waypoints
const MapClickHandler = ({ onAddWaypoint }) => {
  useMapEvents({
    click(e) {
      onAddWaypoint([e.latlng.lat, e.latlng.lng]);
    }
  });
  return null;
};

const MapComponent = ({ shipLocation, waypoints, routePath, onAddWaypoint }) => {
  return (
    <MapContainer 
      center={[shipLocation.lat, shipLocation.lon]} 
      zoom={3} 
      style={{ height: '100%', width: '100%' }}
      className="leaflet-map-custom"
    >
      <LayersControl position="topright">
        <LayersControl.BaseLayer checked name="Satellite">
          <LayerGroup>
            <TileLayer
              attribution='&copy; <a href="https://www.esri.com/">Esri</a>'
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            />
            <TileLayer
              url="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}"
            />
          </LayerGroup>
        </LayersControl.BaseLayer>
        
        <LayersControl.BaseLayer name="Terrain">
          <TileLayer
            attribution='Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a>'
            url="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
          />
        </LayersControl.BaseLayer>
      </LayersControl>
      
      <MapClickHandler onAddWaypoint={onAddWaypoint} />

      {/* Render waypoints and the route connecting them */}
      {waypoints.map((wp, index) => (
        <Marker key={index} position={wp} />
      ))}
      {routePath && routePath.length > 1 && (
        <Polyline positions={routePath} color="var(--primary)" weight={3} dashArray="5, 10" />
      )}

      {/* Render the Ship */}
      <Marker position={[shipLocation.lat, shipLocation.lon]} icon={shipIcon} />
    </MapContainer>
  );
};

export default MapComponent;
