cmake_minimum_required(VERSION 3.14)
project(ZephyrusRLManager)

set(CMAKE_CXX_STANDARD 20)

# Find LibTorch (PyTorch C++ API)
find_package(Torch REQUIRED)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${TORCH_CXX_FLAGS}")

# Find NVIDIA ML
find_library(NVML_LIBRARY nvidia-ml)
include_directories(/opt/cuda/include)
# Fetch FTXUI for the terminal interface
include(FetchContent)
FetchContent_Declare(ftxui 
    GIT_REPOSITORY https://github.com/ArthurSonzogni/FTXUI
    GIT_TAG main
  )
FetchContent_MakeAvailable(ftxui)

add_executable(rog_rl_service 
    src/main.cpp 
    src/telemetry.cpp 
    src/agent.cpp
)

target_link_libraries(rog_rl_service 
    ${TORCH_LIBRARIES} 
    ${NVML_LIBRARY} 
    ftxui::component
    ftxui::dom
    ftxui::screen
)
