#include <ftxui/component/component.hpp>
#include <ftxui/component/screen_interactive.hpp>
#include <ftxui/dom/elements.hpp>
#include <thread>
#include <atomic>
#include <iomanip>
#include <sstream>
#include <algorithm> // Required for std::clamp
#include "agent.h" 

using namespace ftxui;

void init_nvml();
void get_gpu_stats(unsigned int* temp, unsigned int* power_mw);
int get_cpu_temp();

// Helper to format floats for the UI
std::string format_float(float val) {
    std::stringstream stream;
    stream << std::fixed << std::setprecision(2) << val;
    return stream.str();
}

int main() {
    bool gpu_available = true;
    try { init_nvml(); } catch (...) { gpu_available = false; }

    // 1. Initialize the RL Agent (Make sure dummy_dqn.pt is in the build folder!)
    RLAgent agent("dummy_dqn.pt");

    std::atomic<int> gpu_temp = 0;
    std::atomic<int> gpu_power = 0;
    std::atomic<int> cpu_temp = 0;

    // Atomics for the UI to read the agent's decisions
    std::atomic<float> act_cpu_pwr{0.0f}, act_gpu_pwr{0.0f}, act_fan{0.0f};

    auto screen = ScreenInteractive::TerminalOutput();

    auto renderer = Renderer([&] {
        auto gpu_box = gpu_available ? 
            vbox({
                text("Temp: " + std::to_string(gpu_temp) + "°C"),
                text("Power: " + std::to_string(gpu_power / 1000) + " W")
            }) : vbox({text("GPU Asleep (Optimus)")});

        return vbox({
            text("ROG Zephyrus G16 RL Performance Manager") | bold | color(Color::Red),
            separator(),
            hbox({
                window(text(" RTX 4070 "), gpu_box) | flex,
                window(text(" Core Ultra 7 "), vbox({
                    text("Temp: " + std::to_string(cpu_temp) + "°C")
                })) | flex,
            }),
            window(text(" RL Agent Output "), vbox({
                text("Δ CPU Power: " + format_float(act_cpu_pwr)),
                text("Δ GPU Power: " + format_float(act_gpu_pwr)),
                text("Δ Fan Speed:   " + format_float(act_fan))
            })),
        });
    });

    std::thread background_loop([&]() {
        while (true) {
            cpu_temp = get_cpu_temp();
            if (gpu_available) {
                unsigned int t = 0, p = 0;
                get_gpu_stats(&t, &p); 
                gpu_temp = t;
                gpu_power = p;
            }

            // 2. Build the state and get the action
            EnvironmentState state = {
                (float)cpu_temp, (float)gpu_temp, 
                25.0f, (float)(gpu_power / 1000), 2000.0f // Hardcoded some missing telemetry for now
            };
            
            std::vector<float> actions = agent.get_action(state);
            act_cpu_pwr = actions[0];
            act_gpu_pwr = actions[1];
            act_fan = actions[2];

            // --- 🚨 HARDWARE SAFETY LAYER 🚨 ---

            // Calculate intended targets (Current State + AI's Delta)
            float target_cpu_pwr = 45.0f + act_cpu_pwr; 
            float target_gpu_pwr = 60.0f + act_gpu_pwr;
            float target_fan_rpm = state.current_fan_rpm + act_fan;

            // Clamp to safe hardware limits for the G16 (2024)
            target_cpu_pwr = std::clamp(target_cpu_pwr, 15.0f, 80.0f);
            target_gpu_pwr = std::clamp(target_gpu_pwr, 35.0f, 115.0f);
            target_fan_rpm = std::clamp(target_fan_rpm, 0.0f, 6000.0f);

            // Thermal Override (The "Oh Shit" safeguard)
            if (cpu_temp > 90 || gpu_temp > 85) {
                target_cpu_pwr = 25.0f;   // Force heavy throttle
                target_gpu_pwr = 40.0f;   // Force heavy throttle
                target_fan_rpm = 6000.0f; // Force fans to 100%
            }

            // Send to Hardware (Leave commented out until the AI is trained!)
            // set_cpu_pl1_limit((long)target_cpu_pwr);
            // set_gpu_power_limit((unsigned int)(target_gpu_pwr * 1000));
            // set_fan_speed(rpm_to_pwm(target_fan_rpm)); 

            screen.PostEvent(Event::Custom); 
            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    });

    screen.Loop(renderer);
    background_loop.join();
    return 0;
}
