import pytest
import math
import sys
import os
import torch
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather_routing.a_star_router import haversine
from navigation.ddpg_agent import ActorNetwork
from predictive_maintenance.anomaly_detector import AnomalyDetector

def test_haversine_distance():
    # Test distance between New York (40.7128, -74.0060) and London (51.5074, -0.1278)
    # Distance is roughly 5570 km
    ny_lat, ny_lon = 40.7128, -74.0060
    lon_lat, lon_lon = 51.5074, -0.1278
    
    distance = haversine(ny_lat, ny_lon, lon_lat, lon_lon)
    assert 5500 < distance < 5650, f"Calculated distance {distance} is outside expected range."

def test_pytorch_actor_network_shapes():
    state_dim = 5
    action_dim = 2
    actor = ActorNetwork(state_dim, action_dim)
    
    dummy_state = torch.randn(1, state_dim)
    output = actor(dummy_state)
    
    assert output.shape == (1, action_dim), "Actor network output shape is incorrect."
    
    # Test tanh bounding
    assert torch.all(output >= -1.0) and torch.all(output <= 1.0), "Actor output not bounded by tanh"

def test_autoencoder_rul_calculation():
    detector = AnomalyDetector(input_features=128)
    
    # Healthy data should give high RUL
    healthy_data = np.zeros(128)
    result = detector.predict(healthy_data)
    assert result['rul_hours'] > 9000
    assert result['requires_maintenance'] is False
    
    # Anomalous data should reduce RUL
    bad_data = np.random.randn(128) * 10.0
    bad_result = detector.predict(bad_data)
    assert bad_result['rul_hours'] < result['rul_hours']
