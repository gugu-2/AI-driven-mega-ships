# 🚢 AI-Driven Mega Ships: Autonomous Cargo Navigation System

This repository contains the architecture, backend models, and frontend command center for a fully autonomous, AI-driven cargo ship system. Designed to emulate a "Tesla for the oceans," this project integrates advanced Reinforcement Learning, predictive maintenance, real-time kinematics, and a Zero-Trust Data Distribution Service (DDS) architecture.

## 🌟 System Overview

The project is divided into an edge-compute maritime backend (simulating the ship's brain) and a web-based Shore Operations Dashboard (simulating the satellite command center). 

---

### Key Features
- **Intelligent Maritime Pathfinding:** Uses an A* algorithm paired with a `global-land-mask` to dynamically calculate safe, water-only routes around continents, entirely avoiding landmasses and simulated storm zones.
- **Continuous Navigation Control:** Integrates a Deep Deterministic Policy Gradient (DDPG) reinforcement learning environment for collision avoidance and COLREGs-compliant steering.
- **Predictive Maintenance:** Utilizes a PyTorch-based Autoencoder to monitor engine vibration anomalies, calculating the Remaining Useful Life (RUL) of massive maritime machinery before catastrophic failure.
- **Zero-Trust Sensor Fusion:** Simulates a secure DDS message bus, applying Kalman filters to noisy sensor data (GPS, Gyro, LIDAR) to provide a single source of truth for the ship's kinematics.
- **Shore Operations Dashboard:** A premium React/Leaflet web dashboard utilizing the *Replicate* design system (cream canvas, hot orange accents) for real-time human oversight, telemetry monitoring, and interactive route overriding.

---

## 🏗️ Architecture

The system is highly modular, reflecting modern distributed systems on edge devices:

- `sensor_fusion/`: Kalman filtering and mock DDS communication interfaces.
- `predictive_maintenance/`: Autoencoder neural networks for anomaly detection.
- `navigation/`: OpenAI Gym-style environment and Actor-Critic models for autonomous steering.
- `weather_routing/`: A* algorithms for dynamic hurricane evasion and intelligent landmass routing.
- `cybersecurity/`: Zero-Trust RBAC and cryptographic payload validation.
- `routing_api.py`: A Flask microservice exposing the pathfinding algorithms to the frontend.
- `shore-dashboard/`: The React + Vite command center UI.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js & npm (for the React dashboard)

### 1. Backend Setup (Routing API & ML Models)
Install the required Python dependencies:
```bash
pip install torch numpy Flask flask-cors global-land-mask pytest
```
Start the Intelligent Pathfinding API (which powers the dashboard map):
```bash
python routing_api.py
```
*The API will run on `http://localhost:5000`.*

### 2. Frontend Setup (Shore Operations Dashboard)
Navigate into the dashboard directory and install the Node dependencies:
```bash
cd shore-dashboard
npm install
```
Start the Vite development server:
```bash
npm run dev
```
*The dashboard will run on `http://localhost:5173`.*

---

## 🗺️ Interactive Dashboard Guide

Once both servers are running, open `http://localhost:5173` in your browser. 
- **Telemetry Wells:** Watch the ship's real-time Speed, Heading, GPS Confidence, and Engine RUL dynamically update based on the sensor fusion mocks.
- **Interactive Map:** The dashboard uses a high-performance Leaflet CartoDB map. **Click anywhere on the map** to drop a waypoint. The React app will ping the Python Flask backend, calculate a safe route avoiding all landmasses, and draw the path instantly.
- **Layers:** Use the layer control in the top-right of the map to switch between the default Satellite (ESRI World Imagery + Labels) and Terrain map views.

---

## 🧪 Testing

The core algorithms and data contracts are covered by a `pytest` suite. To run the verification tests:
```bash
pytest tests/
```

---
*Built as a conceptual architecture for next-generation automated maritime logistics.*
