"""
Perception Simulator
Generates mock data for LiDAR, Radar, and GPS to test Sensor Fusion.
"""
import random
import time
from datetime import datetime

def generate_mock_gps():
    # Adds gaussian noise to true position
    true_lat, true_lon = 35.0, -120.0
    lat = true_lat + random.gauss(0, 0.0001)
    lon = true_lon + random.gauss(0, 0.0001)
    return {"timestamp": datetime.now(), "lat": lat, "lon": lon}

def generate_mock_lidar_radar():
    # Simulates detecting a dynamic obstacle
    obstacle_distance = random.uniform(50.0, 300.0)
    return {"timestamp": datetime.now(), "closest_obstacle_m": obstacle_distance}

if __name__ == "__main__":
    for _ in range(5):
        print(f"GPS: {generate_mock_gps()}")
        print(f"LiDAR: {generate_mock_lidar_radar()}")
        time.sleep(1)
