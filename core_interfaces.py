"""
Core Interfaces and Protocols for Autonomous Cargo Ship Subsystems.
This module defines the Data Distribution Service (DDS) messages and 
API contracts between the various subsystems of the floating factory.
"""

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

# --- Sensor Fusion & SSoT ---
@dataclass
class ShipState:
    """The Single Source of Truth (SSoT) emitted by Sensor Fusion."""
    timestamp: datetime
    latitude: float
    longitude: float
    heading: float
    speed_knots: float
    confidence_score: float

# --- Navigation & Path Planning ---
@dataclass
class TrajectoryCommand:
    """Command sent to the propulsion and rudder systems."""
    target_heading: float
    target_speed: float
    is_colregs_evasion: bool
    
# --- Weather Routing ---
@dataclass
class MetoceanData:
    """Processed weather data for the routing engine."""
    timestamp: datetime
    wind_speed: float
    wave_height: float
    storm_probability: float

# --- Machinery Monitoring ---
@dataclass
class ComponentHealth:
    """Health score and Remaining Useful Life for a specific engine component."""
    component_id: str
    health_score: float # 0.0 to 100.0
    remaining_useful_life_hours: int
    requires_maintenance: bool

# --- Communication System ---
@dataclass
class TelemetryPacket:
    """Compressed telemetry packet sent to the Shore Operations Center."""
    state: ShipState
    critical_alerts: List[str]
    link_latency_ms: int

class DDSPublisher:
    """Mock interface for the DDS Publish/Subscribe bus."""
    def publish(self, topic: str, data: any):
        pass

class DDSSubscriber:
    def subscribe(self, topic: str, callback):
        pass
