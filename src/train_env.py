import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pynvml
import time
import os
import glob

class ZephyrusThermalEnv(gym.Env):
    def __init__(self):
        super(ZephyrusThermalEnv, self).__init__()
        
        # Action: [Delta CPU Power, Delta GPU Power, Delta Fan RPM]
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)
        # Observation: [CPU Temp, GPU Temp, CPU Pwr, GPU Pwr, Fan RPM]
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(5,), dtype=np.float32)
        
        self.current_step = 0
        self.max_steps = 600 # 10-minute training epoch
        
        # Initialize NVIDIA API
        pynvml.nvmlInit()
        self.gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)

        # Baseline hardware states
        self.current_cpu_pwr_w = 45.0
        self.current_gpu_pwr_w = 60.0
        self.current_fan_rpm = 3000.0

    def get_real_telemetry(self):
        # Read Intel CPU Temp
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            cpu_temp = float(f.read().strip()) / 1000.0
            
        # Read NVIDIA GPU Temp & Power
        gpu_temp = float(pynvml.nvmlDeviceGetTemperature(self.gpu_handle, pynvml.NVML_TEMPERATURE_GPU))
        gpu_power = float(pynvml.nvmlDeviceGetPowerUsage(self.gpu_handle)) / 1000.0 # Convert mW to W
        
        return cpu_temp, gpu_temp, gpu_power

    def step(self, action):
        self.current_step += 1

        # 1. TRANSLATE AI ACTIONS TO PHYSICAL TARGETS
        self.current_cpu_pwr_w = np.clip(self.current_cpu_pwr_w + (action[0] * 10), 15.0, 80.0)
        self.current_gpu_pwr_w = np.clip(self.current_gpu_pwr_w + (action[1] * 10), 35.0, 115.0)
        self.current_fan_rpm = np.clip(self.current_fan_rpm + (action[2] * 1000), 0.0, 6000.0)

        # 2. ACTUATE THE HARDWARE (Requires sudo)
        
        # --- Intel CPU Power Limit ---
        # --- Intel CPU Power Limit (WORKS) ---
        cpu_uw = int(self.current_cpu_pwr_w * 1000000)
        os.system(f"echo {cpu_uw} > /sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw")
        
        # --- NVIDIA GPU Power Limit (LOCKED ON LAPTOPS) ---
        # We comment this out because the VBIOS won't let us write to it.
        # gpu_mw = int(self.current_gpu_pwr_w * 1000)
        # pynvml.nvmlDeviceSetPowerManagementLimit(self.gpu_handle, gpu_mw)
        
        # --- Asus Zephyrus Fan Control (WORKS) ---
        pwm_val = max(0, min(255, int((self.current_fan_rpm / 6000.0) * 255)))
        asus_hwmon = glob.glob('/sys/devices/platform/asus-nb-wmi/hwmon/hwmon*/pwm1')
        if asus_hwmon:
            os.system(f"echo 1 > {asus_hwmon[0]}_enable")
            os.system(f"echo {pwm_val} > {asus_hwmon[0]}")

        # 3. LET THE HEATSINK SOAK
        time.sleep(1.0)

        # 4. MEASURE THE REAL CONSEQUENCES
        cpu_temp, gpu_temp, gpu_power_actual = self.get_real_telemetry()

        # 5. THE REAL-WORLD REWARD FUNCTION
        reward = 0.0
        
        # Reward 1: Maximize stable power draw
        reward += (self.current_cpu_pwr_w * 0.1)
        reward += (self.current_gpu_pwr_w * 0.1)
        
        # Penalty 1: Thermal limits
        if cpu_temp > 90.0: reward -= (cpu_temp - 90.0) * 5.0
        if gpu_temp > 85.0: reward -= (gpu_temp - 85.0) * 5.0
            
        # Penalty 2: Acoustic limits
        reward -= (self.current_fan_rpm / 6000.0) * 2.0 

        # Normalize state for the AI brain [0.0 to 1.0]
        next_state = np.array([
            cpu_temp / 100.0, 
            gpu_temp / 100.0, 
            self.current_cpu_pwr_w / 100.0, 
            self.current_gpu_pwr_w / 150.0, 
            self.current_fan_rpm / 6000.0
        ], dtype=np.float32)

        terminated = bool(self.current_step >= self.max_steps)
        return next_state, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.current_step = 0
        cpu_temp, gpu_temp, gpu_power = self.get_real_telemetry()
        initial_state = np.array([cpu_temp/100, gpu_temp/100, 45/100, 60/150, 3000/6000], dtype=np.float32)
        return initial_state, {}
