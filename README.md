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
