cmake_minimum_required(VERSION 3.15)
project(exercize)

set(CMAKE_CXX_STANDARD 20)

find_package(aws-cpp-sdk-s3 CONFIG REQUIRED)
find_package(CURL REQUIRED)
find_package(ZLIB REQUIRED)

add_executable(load_crawl ./load_crawl.cpp)

target_link_libraries(load_crawl PRIVATE CURL::libcurl ZLIB::ZLIB)