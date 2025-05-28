cmake_minimum_required(VERSION 3.15)
project(data_downloader)

set(CMAKE_CXX_STANDARD 20)

find_package(CURL REQUIRED)
find_package(nlohmann_json REQUIRED)

add_executable(load_data ./data_loader.cpp)

target_link_libraries(load_data PRIVATE CURL::libcurl nlohmann_json::nlohmann_json)