"""
Predictive Maintenance using a PyTorch Autoencoder for Vibration Data.
Calculates Anomaly Score (Reconstruction MSE) and maps it to Remaining Useful Life (RUL).
"""
import torch
import torch.nn as nn
import numpy as np

# --- PyTorch Autoencoder ---

class EngineVibrationAutoencoder(nn.Module):
    def __init__(self, input_features=128):
        super(EngineVibrationAutoencoder, self).__init__()
        # Encoder: compress high-freq vibration data
        self.encoder = nn.Sequential(
            nn.Linear(input_features, 64),
            nn.ReLU(),
            nn.Linear(64, 16),
            nn.ReLU()
        )
        # Decoder: reconstruct data
        self.decoder = nn.Sequential(
            nn.Linear(16, 64),
            nn.ReLU(),
            nn.Linear(64, input_features)
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# --- Anomaly & Prognostic Logic ---

class AnomalyDetector:
    def __init__(self, input_features=128):
        self.device = torch.device("cpu")
        self.model = EngineVibrationAutoencoder(input_features).to(self.device)
        self.loss_fn = nn.MSELoss()
        
        # Survival Analysis Baseline Parameters
        self.healthy_baseline_loss = 0.05
        self.critical_failure_loss = 2.0
        self.max_rul_hours = 10000.0 # Expected life of a healthy component

    def predict(self, raw_vibration_data: np.ndarray) -> dict:
        """
        Ingests vibration data array, runs inference, and returns RUL.
        """
        tensor_data = torch.FloatTensor(raw_vibration_data).unsqueeze(0).to(self.device)
        
        self.model.eval()
        with torch.no_grad():
            reconstructed = self.model(tensor_data)
            
        # Calculate Reconstruction Error (Anomaly Score)
        mse_loss = self.loss_fn(reconstructed, tensor_data).item()
        
        # Prognostics: Map MSE to RUL using exponential degradation assumption
        # If loss is below baseline, it's fully healthy. 
        # As loss approaches critical, RUL decays exponentially.
        if mse_loss <= self.healthy_baseline_loss:
            rul_hours = self.max_rul_hours
            requires_maintenance = False
        else:
            # Simple regression formula for demonstration
            degradation_ratio = (mse_loss - self.healthy_baseline_loss) / (self.critical_failure_loss - self.healthy_baseline_loss)
            rul_hours = max(0.0, self.max_rul_hours * (1.0 - degradation_ratio))
            requires_maintenance = rul_hours < 500.0 # Alert if < 500 hours left
            
        return {
            "anomaly_score": mse_loss,
            "rul_hours": round(rul_hours, 1),
            "requires_maintenance": requires_maintenance
        }

if __name__ == "__main__":
    print("Initializing PyTorch Autoencoder...")
    detector = AnomalyDetector(input_features=128)
    
    # 1. Healthy Data Test
    healthy_data = np.zeros(128) # Perfectly predictable
    health_result = detector.predict(healthy_data)
    print(f"\n[Healthy Test] MSE: {health_result['anomaly_score']:.4f} | RUL: {health_result['rul_hours']}h | Alert: {health_result['requires_maintenance']}")
    
    # 2. Anomalous Data Test
    anomalous_data = np.random.randn(128) * 5.0 # Highly erratic vibration
    anomaly_result = detector.predict(anomalous_data)
    print(f"\n[Anomaly Test] MSE: {anomaly_result['anomaly_score']:.4f} | RUL: {anomaly_result['rul_hours']}h | Alert: {anomaly_result['requires_maintenance']}")
