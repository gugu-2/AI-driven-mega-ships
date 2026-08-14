"""
Pub/Sub DDS Mock
Simulates the ROS 2 Data Distribution Service with Zero Trust Security.
"""
import threading
from collections import defaultdict
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cybersecurity.zero_trust_auth import ZeroTrustValidator

class DDSBroker:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DDSBroker, cls).__new__(cls)
                cls._instance.subscribers = defaultdict(list)
                cls._instance.validator = ZeroTrustValidator()
        return cls._instance

    def subscribe(self, topic: str, callback, node_id: str, cert: str):
        if self.validator.authenticate_node(node_id, cert):
            self.subscribers[topic].append(callback)
            return True
        return False

    def publish(self, topic: str, data: any, node_id: str, cert: str):
        if self.validator.authenticate_node(node_id, cert):
            for callback in self.subscribers.get(topic, []):
                callback(data)
            return True
        return False

def example_subscriber(data):
    print(f"Received data: {data}")

if __name__ == "__main__":
    broker = DDSBroker()
    # Attempt unauthorized subscribe
    broker.subscribe("ship_state", example_subscriber, "hacker_node", "fake_cert")
    
    # Authorized subscribe
    broker.subscribe("ship_state", example_subscriber, "nav_computer_1", "valid_cert_nav1")
    
    # Authorized publish
    broker.publish("ship_state", {"lat": 10.0, "lon": 20.0}, "sensor_fusion_edge", "valid_cert_sf")
