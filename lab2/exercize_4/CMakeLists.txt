cmake_minimum_required(VERSION 3.15)
project(json_to_csv)

set(CMAKE_CXX_STANDARD 20)

find_package(nlohmann_json REQUIRED)

add_executable(json_to_csv ./json_to_csv.cpp)

target_link_libraries(json_to_csv PRIVATE nlohmann_json::nlohmann_json)

#---- Libraries for load_postgres----

find_package(libpqxx REQUIRED)

add_executable(load_to_postgres ./load_to_postgres.cpp)

target_link_libraries(load_to_postgres PRIVATE libpqxx::pqxx)