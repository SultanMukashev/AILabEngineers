cmake_minimum_required(VERSION 3.15)

set(CMAKE_CXX_STANDARD 20)

find_package(libzip CONFIG REQUIRED)

add_executable(extract_data ./data_extraction.cpp)

target_link_libraries(extract_data PRIVATE libzip::zip)