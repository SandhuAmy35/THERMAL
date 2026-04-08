#include <nvml.h>
#include <fstream>
#include <iostream>
#include <string>
#include <filesystem>

// --- NVIDIA GPU (RTX 4070) ---
void init_nvml() {
    nvmlInit();
}


// Reads the standard Linux thermal zone
int get_cpu_temp() {
    std::ifstream file("/sys/class/thermal/thermal_zone0/temp");
    int temp = 0;
    if (file >> temp) {
        return temp / 1000; // Sysfs reports in millidegrees Celsius
    }
    return 0; 
}

// Finds the specific hwmon directory for the Asus WMI driver
std::string find_asus_hwmon() {
    std::string base_path = "/sys/devices/platform/asus-nb-wmi/hwmon/";
    for (const auto& entry : std::filesystem::directory_iterator(base_path)) {
        return entry.path().string(); // Usually hwmon2, hwmon3, etc.
    }
    return "";
}

// pwm_value ranges from 0 (off) to 255 (max speed)
void set_fan_speed(int pwm_value) {
    std::string hwmon_path = find_asus_hwmon();
    if (hwmon_path.empty()) return;

    // pwm1_enable = 1 puts the fan in manual mode
    std::ofstream enable_file(hwmon_path + "/pwm1_enable");
    enable_file << 1; 

    // Write the actual speed
    std::ofstream pwm_file(hwmon_path + "/pwm1");
    pwm_file << pwm_value;
}

void get_gpu_stats(unsigned int* temp, unsigned int* power_mw) {
    nvmlDevice_t device;
    nvmlReturn_t result;

    // 1. Grab the RTX 4070
    result = nvmlDeviceGetHandleByIndex(0, &device);
    if (result != NVML_SUCCESS) {
        *temp = 0; *power_mw = 0;
        return; 
    }

    // 2. Read Temp
    result = nvmlDeviceGetTemperature(device, NVML_TEMPERATURE_GPU, temp);
    if (result != NVML_SUCCESS) *temp = 0;

    // 3. Read Power (This often requires sudo)
    result = nvmlDeviceGetPowerUsage(device, power_mw);
    if (result != NVML_SUCCESS) *power_mw = 0;
}

void set_gpu_power_limit(unsigned int limit_mw) {
    nvmlDevice_t device;
    nvmlDeviceGetHandleByIndex(0, &device);
    // Note: Requires root privileges
    nvmlDeviceSetPowerManagementLimit(device, limit_mw); 
}

// --- Intel CPU (Core Ultra 7 155H) ---
// Uses Linux powercap subsystem
long get_cpu_power_uw() {
    std::ifstream file("/sys/class/powercap/intel-rapl:0/energy_uj");
    long energy;
    file >> energy;
    return energy; // You must sample this over time (delta energy / delta time = power)
}

void set_cpu_pl1_limit(long watts) {
    // Requires root
    std::ofstream file("/sys/class/powercap/intel-rapl:0/constraint_0_power_limit_uw");
    file << (watts * 1000000); 
}
