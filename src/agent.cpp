#include "agent.h"
#include <iostream>

RLAgent::RLAgent(const std::string& model_path) {
    try {
        module = torch::jit::load(model_path);
    } catch (const c10::Error& e) {
        std::cerr << "Error loading model\n";
    }
}

std::vector<float> RLAgent::get_action(const EnvironmentState& state) {
    // 1. Force the 1D array into a 2D "batch" matrix: [1 row, 5 columns]
    torch::Tensor input = torch::tensor({
        state.cpu_temp, state.gpu_temp, 
        state.cpu_power, state.gpu_power, state.current_fan_rpm
    }).view({1, 5});

    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(input);

    // 2. Run inference
    torch::Tensor output = module.forward(inputs).toTensor();
    
    // 3. Extract the outputs from the first row [0] of the batch
    return {
        output[0][0].item<float>(), // CPU Power Delta
        output[0][1].item<float>(), // GPU Power Delta
        output[0][2].item<float>()  // Fan Speed Delta
    };
}
