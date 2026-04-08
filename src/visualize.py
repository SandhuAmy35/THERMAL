#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation

def animate(i):
    try:
        data = pd.read_csv('training_log.csv')
    except:
        return # File might be locked during a write

    if data.empty: return

    plt.cla() # Clear current axis
    
    # Subplot 1: Learning Curve (Rewards)
    ax1 = plt.subplot(2, 1, 1)
    plt.plot(data['step'], data['reward'].rolling(window=10).mean(), label='Avg Reward', color='green')
    plt.title('RL Learning Progress')
    plt.ylabel('Reward')
    plt.legend()

    # Subplot 2: Hardware Telemetry
    ax2 = plt.subplot(2, 1, 2)
    plt.plot(data['step'], data['cpu_temp'], label='CPU Temp', color='red', alpha=0.6)
    plt.plot(data['step'], data['gpu_temp'], label='GPU Temp', color='orange', alpha=0.6)
    plt.axhline(y=90, color='darkred', linestyle='--', label='Throttle Wall')
    plt.ylabel('Temp (°C)')
    plt.xlabel('Steps')
    plt.legend()
    plt.tight_layout()

fig = plt.figure(figsize=(10, 8))
ani = FuncAnimation(fig, animate, interval=2000, cache_frame_data=False)
plt.show()
