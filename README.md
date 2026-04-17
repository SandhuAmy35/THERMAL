# Zephyrus-RL: AI-Driven Thermal & Power Manager

**Zephyrus-RL** is a high-performance C++ daemon and Reinforcement Learning (RL) framework designed to dynamically optimize the thermals and power limits of the **ROG Zephyrus G16 (2024)**. 

Instead of relying on static, manufacturer-defined fan curves, this project uses a **Proximal Policy Optimization (PPO)** agent to learn the specific thermal characteristics of the laptop's vapor chamber and adjust power limits (PL1/PL2) and fan speeds in real-time to maximize sustained performance.

---

## 🚀 Key Features
* **Real-time C++ Daemon:** Built with C++20, utilizing **FTXUI** for a responsive terminal-based dashboard.
* **Neural Inference:** Uses **LibTorch** (PyTorch C++ frontend) to run the trained RL model with minimal overhead.
* **Live Hardware Training:** A custom **OpenAI Gymnasium** environment that trains the AI directly on physical hardware telemetry.
* **Safety Layer:** A hardcoded C++ gatekeeper that intercepts AI decisions and enforces physical safety limits (e.g., maximum temps and power draws).
* **Optimus-Aware:** Gracefully handles NVIDIA GPU sleep states to prevent battery drain and unnecessary wake-ups.

---

## 🏗 Architecture
The system operates in a closed-loop feedback system:
1.  **Telemetry:** Collects CPU/GPU temps and power draw via Linux `sysfs` and NVIDIA **NVML**.
2.  **Policy:** Feeds normalized telemetry into a TorchScript neural network.
3.  **Actuation:** The agent outputs deltas for CPU power and fan speeds.
4.  **Safety:** Decisions are clamped by a C++ safety layer before being written to hardware registers.



---

## 🛠 Tech Stack
* **Languages:** C++20, Python 3.13+
* **Frameworks:** LibTorch (C++), Stable Baselines3 (PPO), Gymnasium
* **Libraries:** FTXUI, Pynvml, CMake
* **Platform:** Linux (Tested on Arch / Omarchy)
* **Hardware Hooks:** Intel RAPL, NVIDIA NVML, Asus WMI

---

## 🚦 Getting Started

### Prerequisites
Ensure you have the following installed on your system:

```bash
# Arch Linux / Omarchy
sudo pacman -S gcc cmake libtorch python-pip pynvml stress# Zephyrus-RL: AI-Driven Thermal & Power Manager
```
**Zephyrus-RL** is a high-performance C++ daemon and Reinforcement Learning (RL) framework designed to dynamically optimize the thermals and power limits of the **ROG Zephyrus G16 (2024)**. 

Instead of relying on static, manufacturer-defined fan curves, this project uses a **Proximal Policy Optimization (PPO)** agent to learn the specific thermal characteristics of the laptop's vapor chamber and adjust power limits (PL1/PL2) and fan speeds in real-time to maximize sustained performance.

---

## 🚀 Key Features
* **Real-time C++ Daemon:** Built with C++20, utilizing **FTXUI** for a responsive terminal-based dashboard.
* **Neural Inference:** Uses **LibTorch** (PyTorch C++ frontend) to run the trained RL model with minimal overhead.
* **Live Hardware Training:** A custom **OpenAI Gymnasium** environment that trains the AI directly on physical hardware telemetry.
* **Safety Layer:** A hardcoded C++ gatekeeper that intercepts AI decisions and enforces physical safety limits (e.g., maximum temps and power draws).
* **Optimus-Aware:** Gracefully handles NVIDIA GPU sleep states to prevent battery drain and unnecessary wake-ups.

---

## 🏗 Architecture
The system operates in a closed-loop feedback system:
1.  **Telemetry:** Collects CPU/GPU temps and power draw via Linux `sysfs` and NVIDIA **NVML**.
2.  **Policy:** Feeds normalized telemetry into a TorchScript neural network.
3.  **Actuation:** The agent outputs deltas for CPU power and fan speeds.
4.  **Safety:** Decisions are clamped by a C++ safety layer before being written to hardware registers.



---

## 🛠 Tech Stack
* **Languages:** C++20, Python 3.13+
* **Frameworks:** LibTorch (C++), Stable Baselines3 (PPO), Gymnasium
* **Libraries:** FTXUI, Pynvml, CMake
* **Platform:** Linux (Tested on Arch / Omarchy)
* **Hardware Hooks:** Intel RAPL, NVIDIA NVML, Asus WMI

---

## 🚦 Getting Started

### Prerequisites
Ensure you have the following installed on your system:
```bash
# Arch Linux / Omarchy
sudo pacman -S gcc cmake libtorch python-pip pynvml stress
```
Installation & Build
Clone the Repo:

```Bash
git clone [https://github.com/SandhuAmy35/Zephyrus-RL.git](https://github.com/SandhuAmy35/Zephyrus-RL.git)
cd Zephyrus-RL
Build the C++ Daemon:
```

```Bash
mkdir build && cd build
cmake ..
make -j$(nproc)
```
Training the Brain
Before running the daemon, the agent must "soak" the hardware to learn the thermal dynamics.

Open a terminal and start a stress test: 
```Bash
stress -c 16
```
In another terminal, run the training script (requires sudo for hardware access):

```Bash
cd src
sudo python train.py
```
The agent will train for approximately 10 minutes and export dummy_dqn.pt to the build/ folder.

🖥 Usage
Once the model is trained, launch the manager:

```Bash
cd build
sudo ./rog_rl_service
```
Dashboard View
RTX 4070 Box: Real-time GPU temp, power, and Optimus status.

Core Ultra 7 Box: Real-time Intel CPU thermal status.

RL Agent Output: Live visualization of the AI's intended power and fan adjustments.

🛡 Hardware Safety Disclaimer
WARNING: This software interacts directly with hardware power registers. While it includes a hardcoded C++ safety layer to prevent overheating, use this at your own risk. The authors are not responsible for any damage to your hardware.

The safety layer enforces:

CPU Limit: 15W - 80W

GPU Limit: 35W - 115W (LOCKED via VBIOS on most G16 models)

Emergency Throttle: Forced 100% fans if Temps > 90°C.

🤝 Contributing
Contributions are welcome! If you have ideas for better reward functions or support for other ROG laptops, feel free to open a PR.
