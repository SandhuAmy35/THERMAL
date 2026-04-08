#pragma once
#include <vector>
#include <string>
#include <torch/script.h>

struct EnvironmentState {
    float cpu_temp;
    float gpu_temp;
    float cpu_power;
    float gpu_power;
    float current_fan_rpm;
};

class RLAgent {
private:
    torch::jit::script::Module module;
public:
    RLAgent(const std::string& model_path);
    std::vector<float> get_action(const EnvironmentState& state);
};
