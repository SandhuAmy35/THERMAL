import torch
import torch.nn as nn
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
from train_env import ZephyrusThermalEnv
import csv

# 1. Custom Callback to log real-time hardware data to CSV
class TelemetryCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(TelemetryCallback, self).__init__(verbose)
        self.log_file = "training_log.csv"
        with open(self.log_file, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(['step', 'reward', 'cpu_temp', 'gpu_temp', 'fan_rpm'])

    def _on_step(self) -> bool:
        # 🚨 THE FIX: Use .unwrapped to bypass the Monitor/VecEnv wrappers
        env = self.training_env.envs[0].unwrapped
        
        # Now we can call your custom hardware function safely
        cpu_temp, gpu_temp, _ = env.get_real_telemetry()
        
        with open(self.log_file, mode='a') as f:
            writer = csv.writer(f)
            writer.writerow([
                self.num_timesteps, 
                self.locals['rewards'][0], 
                cpu_temp, 
                gpu_temp, 
                env.current_fan_rpm
            ])
        return True

# 2. Setup Environment and Model
env = ZephyrusThermalEnv()

print("Initializing PPO Agent on RTX 4070...")
# This defines 'model' - the line that was missing!
model = PPO("MlpPolicy", env, verbose=1, device="cuda")

# 3. Start Training with Callback
print("Starting real-time hardware training loop...")
callback = TelemetryCallback()
model.learn(total_timesteps=600, callback=callback)
print("Training complete!")

# 4. Clean Export for C++
model.policy.to("cpu")
model.policy.eval()

class ExportWrapper(nn.Module):
    def __init__(self, policy):
        super().__init__()
        self.policy = policy
    def forward(self, obs):
        features = self.policy.extract_features(obs)
        latent_pi, _ = self.policy.mlp_extractor(features)
        return self.policy.action_net(latent_pi)

clean_model = ExportWrapper(model.policy)
dummy_input = torch.randn(1, 5)
traced_module = torch.jit.trace(clean_model, dummy_input)

save_path = "../build/dummy_dqn.pt"
traced_module.save(save_path)
print(f"Exported clean brain to {save_path}")
