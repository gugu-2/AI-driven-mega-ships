import math
import heapq
from flask import Flask, request, jsonify
from flask_cors import CORS
from global_land_mask import globe

app = Flask(__name__)
CORS(app)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def get_neighbors(node, step=1):
    lat, lon = node
    neighbors = []
    for dlat in [-step, 0, step]:
        for dlon in [-step, 0, step]:
            if dlat == 0 and dlon == 0:
                continue
            n_lat = lat + dlat
            n_lon = lon + dlon
            
            # Wrap longitude around the globe
            if n_lon > 180:
                n_lon -= 360
            elif n_lon < -180:
                n_lon += 360
                
            # Clamp latitude
            if -90 <= n_lat <= 90:
                neighbors.append((n_lat, n_lon))
    return neighbors

def a_star_route(start, goal, step=2):
    # Align to grid
    start_grid = (round(start[0]/step)*step, round(start[1]/step)*step)
    goal_grid = (round(goal[0]/step)*step, round(goal[1]/step)*step)
    
    # Priority queue: (f_score, node)
    open_set = []
    heapq.heappush(open_set, (0, start_grid))
    
    came_from = {}
    
    g_score = {start_grid: 0}
    f_score = {start_grid: haversine(start_grid[0], start_grid[1], goal_grid[0], goal_grid[1])}
    
    max_iterations = 20000
    iterations = 0
    
    while open_set:
        iterations += 1
        if iterations > max_iterations:
            print("Max iterations reached")
            break
            
        _, current = heapq.heappop(open_set)
        
        if haversine(current[0], current[1], goal_grid[0], goal_grid[1]) <= step * 1.5:
            # We reached the goal (or close enough)
            path = [goal]
            path.append(current)
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.append(start)
            path.reverse()
            return path
            
        for neighbor in get_neighbors(current, step):
            # Check if land
            if globe.is_land(neighbor[0], neighbor[1]):
                continue
                
            tentative_g_score = g_score[current] + haversine(current[0], current[1], neighbor[0], neighbor[1])
            
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + haversine(neighbor[0], neighbor[1], goal_grid[0], goal_grid[1])
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                
    # Fallback if no path found
    return [start, goal]

@app.route('/route', methods=['POST'])
def route():
    data = request.json
    waypoints = data.get('waypoints', [])
    
    if len(waypoints) < 2:
        return jsonify({"path": waypoints})
        
    full_path = []
    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        goal = waypoints[i+1]
        
        # Calculate A* path segment avoiding land (using 2-degree step for speed)
        segment = a_star_route(start, goal, step=2)
        
        if i == 0:
            full_path.extend(segment)
        else:
            # Avoid duplicating the shared waypoint
            full_path.extend(segment[1:])
            
    return jsonify({"path": full_path})

if __name__ == '__main__':
    app.run(port=5000)
