"""
Zero Trust Architecture and Authentication Module.
Validates mock TPM 2.0 hardware certificates before allowing nodes to communicate.
"""

class ZeroTrustValidator:
    def __init__(self):
        # A mock list of allowed hardware certificates (TPM signatures)
        self.authorized_nodes = {
            "nav_computer_1": "valid_cert_nav1",
            "sensor_fusion_edge": "valid_cert_sf",
            "predictive_maintenance_node": "valid_cert_pm"
        }

    def authenticate_node(self, node_id: str, provided_cert: str) -> bool:
        """
        Validates if a node is authorized to join the DDS bus.
        """
        if node_id not in self.authorized_nodes:
            print(f"[SECURITY ALERT] Node {node_id} is unknown. Access Denied.")
            return False
        
        if self.authorized_nodes[node_id] != provided_cert:
            print(f"[SECURITY ALERT] Node {node_id} provided invalid cert. Access Denied.")
            return False
            
        print(f"[SECURITY] Node {node_id} successfully authenticated via Zero Trust.")
        return True
