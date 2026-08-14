"""
Simple Kalman Filter Mock
Fuses noisy GPS and IMU data to produce a stable Ship State.
"""
import random

class ShipStateEKF:
    def __init__(self):
        self.estimated_lat = 35.0
        self.estimated_lon = -120.0
        self.uncertainty = 1.0

    def predict(self, imu_dx, imu_dy):
        # Predict step using IMU
        self.estimated_lat += imu_dx
        self.estimated_lon += imu_dy
        self.uncertainty += 0.1 # Uncertainty grows without GPS

    def update(self, gps_lat, gps_lon, gps_noise_var=0.05):
        # Update step using GPS
        kalman_gain = self.uncertainty / (self.uncertainty + gps_noise_var)
        self.estimated_lat += kalman_gain * (gps_lat - self.estimated_lat)
        self.estimated_lon += kalman_gain * (gps_lon - self.estimated_lon)
        self.uncertainty = (1 - kalman_gain) * self.uncertainty

    def get_state(self):
        return {"lat": self.estimated_lat, "lon": self.estimated_lon, "uncertainty": self.uncertainty}

if __name__ == "__main__":
    ekf = ShipStateEKF()
    for _ in range(10):
        ekf.predict(0.001, 0.001) # constant motion
        # Noisy GPS reading
        gps_lat = 35.0 + 0.001 * _ + random.gauss(0, 0.005)
        gps_lon = -120.0 + 0.001 * _ + random.gauss(0, 0.005)
        ekf.update(gps_lat, gps_lon)
        print(f"EKF State: {ekf.get_state()}")
