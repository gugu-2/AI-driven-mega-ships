"""
Deep Deterministic Policy Gradient (DDPG) Agent for COLREGs Navigation.
Implements PyTorch Actor and Critic Neural Networks.
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# --- PyTorch Models ---

class ActorNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(ActorNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.out = nn.Linear(256, action_dim)
        self.relu = nn.ReLU()
        self.tanh = nn.Tanh() # Actions bounded between -1 and 1

    def forward(self, state):
        x = self.relu(self.fc1(state))
        x = self.relu(self.fc2(x))
        return self.tanh(self.out(x))

class CriticNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(CriticNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim + action_dim, 256)
        self.fc2 = nn.Linear(256, 256)
        self.out = nn.Linear(256, 1) # Outputs Q-value
        self.relu = nn.ReLU()

    def forward(self, state, action):
        x = torch.cat([state, action], dim=1)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        return self.out(x)

# --- Agent Logic ---

class DDPGAgent:
    def __init__(self, state_dim, action_dim):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize Actor and Critic
        self.actor = ActorNetwork(state_dim, action_dim).to(self.device)
        self.critic = CriticNetwork(state_dim, action_dim).to(self.device)
        
        # Optimizers
        self.actor_optimizer = optim.Adam(self.actor.parameters(), lr=1e-4)
        self.critic_optimizer = optim.Adam(self.critic.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()

    def select_action(self, state_array):
        """Returns a deterministic action based on the state."""
        state_tensor = torch.FloatTensor(state_array).unsqueeze(0).to(self.device)
        self.actor.eval()
        with torch.no_grad():
            action = self.actor(state_tensor).cpu().numpy().flatten()
        self.actor.train()
        return action

    def train_step(self, states, actions, rewards, next_states, dones):
        """Mock training step to verify gradients flow."""
        states = torch.FloatTensor(states).to(self.device)
        actions = torch.FloatTensor(actions).to(self.device)
        rewards = torch.FloatTensor(rewards).unsqueeze(1).to(self.device)
        
        # Train Critic
        current_Q = self.critic(states, actions)
        critic_loss = self.loss_fn(current_Q, rewards) # Simplified target
        
        self.critic_optimizer.zero_grad()
        critic_loss.backward()
        self.critic_optimizer.step()
        
        # Train Actor
        actor_loss = -self.critic(states, self.actor(states)).mean()
        
        self.actor_optimizer.zero_grad()
        actor_loss.backward()
        self.actor_optimizer.step()
        
        return critic_loss.item(), actor_loss.item()

if __name__ == "__main__":
    print("Initializing PyTorch DDPG Agent...")
    agent = DDPGAgent(state_dim=5, action_dim=2) # State: [lat, lon, heading, speed, rudder], Action: [rudder_delta, speed_delta]
    print(f"Actor Model:\n{agent.actor}")
    print(f"Critic Model:\n{agent.critic}")
    
    # Test forward pass
    dummy_state = np.array([0.0, 0.0, 45.0, 10.0, 0.0])
    action = agent.select_action(dummy_state)
    print(f"Forward Pass Action output (scaled -1 to 1): {action}")
