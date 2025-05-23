cmake_minimum_required(VERSION 3.15)
project(exercize_5)

set(CMAKE_CXX_STANDARD 20)

find_package(libpqxx REQUIRED)

add_executable(process_csv
    process_csv.cpp
    sql_datatype/SqlType.cpp
    SQL_Table/Sql_table.cpp
)

target_include_directories(process_csv PRIVATE
    ${PROJECT_SOURCE_DIR}/sql_datatype
    ${PROJECT_SOURCE_DIR}/SQL_Table
)

target_link_libraries(process_csv PRIVATE libpqxx::pqxx)