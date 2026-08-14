"""
High-Fidelity Gymnasium-style environment for training the Navigation AI.
Simulates realistic ship hydrodynamics (inertia, wind drift) and COLREGs Target Ships.
"""
import math
import random

class AutonomousShipEnv:
    def __init__(self):
        self.state = {
            "lat": 0.0, "lon": 0.0, 
            "heading": 0.0, "speed": 10.0,
            "rudder_angle": 0.0 # Introduces inertia/delay
        }
        self.goal = {"lat": 1.0, "lon": 1.0}
        
        # Dynamic obstacles for COLREGs training
        self.target_ships = [
            {"lat": 0.5, "lon": 0.5, "heading": 180.0, "speed": 12.0, "type": "head-on"},
            {"lat": 0.2, "lon": 0.8, "heading": 270.0, "speed": 8.0, "type": "crossing-starboard"}
        ]
        
    def reset(self):
        self.state = {"lat": 0.0, "lon": 0.0, "heading": 0.0, "speed": 10.0, "rudder_angle": 0.0}
        return self.state

    def step(self, action):
        # Action is [desired_rudder_angle, desired_speed]
        
        # 1. Ship Hydrodynamics (Inertia & Turning Circle)
        # Rudder cannot change instantly; it turns slowly
        rudder_delta = action[0] - self.state["rudder_angle"]
        self.state["rudder_angle"] += max(-5.0, min(5.0, rudder_delta)) # Max 5 deg per second turn rate
        
        # Heading changes based on current rudder angle (inertia)
        self.state["heading"] += self.state["rudder_angle"] * 0.1
        
        # Speed changes slowly (massive momentum)
        speed_delta = action[1] - self.state["speed"]
        self.state["speed"] += max(-0.5, min(0.5, speed_delta))
        
        # 2. Environmental Factors (Wind Drift)
        wind_drift_lat = -0.0001 # Blowing South
        
        # Kinematic update with drift
        self.state["lat"] += (self.state["speed"] * 0.001 * math.cos(math.radians(self.state["heading"]))) + wind_drift_lat
        self.state["lon"] += (self.state["speed"] * 0.001 * math.sin(math.radians(self.state["heading"])))
        
        # 3. COLREGs Collision Detection
        colregs_penalty = 0
        for ship in self.target_ships:
            # Move target ships
            ship["lat"] += ship["speed"] * 0.001 * math.cos(math.radians(ship["heading"]))
            ship["lon"] += ship["speed"] * 0.001 * math.sin(math.radians(ship["heading"]))
            
            # Check distance (CPA - Closest Point of Approach)
            dist = math.sqrt((ship["lat"] - self.state["lat"])**2 + (ship["lon"] - self.state["lon"])**2)
            if dist < 0.1: # Near miss or collision
                colregs_penalty -= 1000
                print(f"⚠️ COLREGs VIOLATION: Dangerous proximity to {ship['type']} vessel!")
        
        # Calculate reward
        distance_to_goal = math.sqrt((self.goal["lat"] - self.state["lat"])**2 + (self.goal["lon"] - self.state["lon"])**2)
        reward = -distance_to_goal + colregs_penalty
        
        done = distance_to_goal < 0.05
        return self.state, reward, done, {}

if __name__ == "__main__":
    env = AutonomousShipEnv()
    print("Initial state:", env.reset())
    print("Simulating 5 seconds of movement...")
    for _ in range(5):
        # AI commands hard starboard to avoid head-on ship
        next_state, reward, done, _ = env.step([35.0, 10.0]) 
    print("Final state:", next_state)
