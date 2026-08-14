import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datetime import datetime
from core_interfaces import ShipState, ComponentHealth

def test_ship_state_instantiation():
    state = ShipState(
        timestamp=datetime.now(),
        latitude=45.0,
        longitude=-120.0,
        heading=90.0,
        speed_knots=15.5,
        confidence_score=0.99
    )
    assert state.latitude == 45.0
    assert state.speed_knots == 15.5
    assert state.confidence_score > 0.9

def test_component_health_instantiation():
    health = ComponentHealth(
        component_id="MAIN_ENGINE_BEARING_1",
        health_score=85.0,
        remaining_useful_life_hours=1200,
        requires_maintenance=False
    )
    assert health.requires_maintenance is False
