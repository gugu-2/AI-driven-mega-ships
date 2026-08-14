"""
A* (A-Star) Pathfinding Algorithm with Spherical Geometry.
Uses the Haversine formula for Great Circle distances and avoids dynamic hurricane zones.
"""
import math
import heapq

# --- Spherical Geometry (Haversine) ---

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    R = 6371.0 # Earth radius in km

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

# --- Weather Overlay ---

class HurricaneSimulator:
    def __init__(self, center_lat, center_lon, radius_km):
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.radius_km = radius_km

    def get_weather_penalty(self, lat, lon):
        """Returns an infinite penalty if inside the hurricane."""
        dist = haversine(self.center_lat, self.center_lon, lat, lon)
        if dist <= self.radius_km:
            return float('inf') # Impassable
        elif dist <= self.radius_km * 1.5:
            return 1000.0 # High risk zone
        return 0.0

# --- A* Algorithm ---

def a_star_routing(start, goal, hurricane):
    """
    Calculates the optimal path on a spherical grid avoiding storms.
    """
    # Using a simple grid for demonstration
    grid_resolution = 1.0 # degrees
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: haversine(start[0], start[1], goal[0], goal[1])}
    
    # Restrict search space to prevent infinite loops in mock
    max_iterations = 2000
    iterations = 0
    
    while open_set and iterations < max_iterations:
        iterations += 1
        current = heapq.heappop(open_set)[1]
        
        # Check if close enough to goal
        if haversine(current[0], current[1], goal[0], goal[1]) < 150: # km
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1] # Reverse path
            
        # Generate neighbors (8-way movement on spherical grid)
        neighbors = [
            (current[0]+grid_resolution, current[1]),
            (current[0]-grid_resolution, current[1]),
            (current[0], current[1]+grid_resolution),
            (current[0], current[1]-grid_resolution),
            (current[0]+grid_resolution, current[1]+grid_resolution),
            (current[0]-grid_resolution, current[1]-grid_resolution),
            (current[0]+grid_resolution, current[1]-grid_resolution),
            (current[0]-grid_resolution, current[1]+grid_resolution)
        ]
        
        for neighbor in neighbors:
            weather_penalty = hurricane.get_weather_penalty(neighbor[0], neighbor[1])
            if weather_penalty == float('inf'):
                continue # Skip impassable nodes
                
            tentative_g_score = g_score[current] + haversine(current[0], current[1], neighbor[0], neighbor[1]) + weather_penalty
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + haversine(neighbor[0], neighbor[1], goal[0], goal[1])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    return None # Path not found

if __name__ == "__main__":
    start_pos = (25.0, -80.0) # Miami
    goal_pos = (51.5, -0.1) # London
    
    # Hurricane in the middle of the Atlantic
    hurricane = HurricaneSimulator(center_lat=40.0, center_lon=-40.0, radius_km=500.0)
    
    print(f"Routing from {start_pos} to {goal_pos}...")
    print(f"Hurricane active at {hurricane.center_lat}, {hurricane.center_lon} (Radius: {hurricane.radius_km}km)")
    
    path = a_star_routing(start_pos, goal_pos, hurricane)
    
    if path:
        print(f"Path found! Waypoints: {len(path)}")
        for i, wp in enumerate(path[::10]): # Print every 10th waypoint
            print(f"  WP {i*10}: Lat {wp[0]:.1f}, Lon {wp[1]:.1f}")
    else:
        print("Routing failed.")
