cmake_minimum_required(VERSION 3.15) # Minimum CMake version
project(load_postgres) # Project name

set(CMAKE_CXX_STANDARD 20)

find_package(libpqxx CONFIG REQUIRED) # Config seeking the needed libraries

add_executable(load_postgres ./load_postgres.cpp) # Creating executable build

target_link_libraries(load_postgres PRIVATE libpqxx::pqxx) # Linking libraries

# ---- AWS SDK setup for a separate file ----

# Find AWS SDK components (example: S3 and Core)
find_package(aws-cpp-sdk-s3 CONFIG REQUIRED)

add_executable(s3_uploader s3_uploader.cpp) # Creating executable build
target_link_libraries(s3_uploader PRIVATE aws-cpp-sdk-s3 aws-cpp-sdk-core) # Linking libraries