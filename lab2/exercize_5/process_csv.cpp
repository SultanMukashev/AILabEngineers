#include <pqxx/pqxx>
#include <filesystem>
#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>

#include "SQL_Table/Sql_table.h"

namespace file_sys = std::filesystem;

/**
 * @brief just turning the line to lower case
 * 
 * @param line the string to be turned to lower case
 * @return a lower case string
 */
std::string toLower(const std::string& line);
/**
 * @brief just turns the \\ in the path to regular /
 * 
 * @param path the path ro be "corrected"
 * @return string with the "corrected" path
 */
std::string correctPath(const std::string& path);
/**
 * @brief finds all paths to csv files in the given directory
 * 
 * @param path a path to the directory to be searched
 * @return std::vector<std::string> with all csv file paths
 */
std::vector<std::string> findAllCsvs(const std::string& path);
/**
 * @brief handles csv file work
 */
Sql_table handleCsv(const std::string& path);
/**
 * @brief fetches the given line(from csv)
 */
std::vector<std::string> fetchLine(const std::string& line);

int main() {
    try {
        // Postgres connection
        pqxx::connection conn("host=localhost port=5433 user=user password=password dbname=mydb");

        if(conn.is_open()) {
            pqxx::work txn(conn); // Transaction
            std::vector<Sql_table> curr_db; // Current database for work

            std::vector<std::string> csv_paths = findAllCsvs("./data");

            // Adding all tables to the database
            for(const std::string& csv : csv_paths) {
                curr_db.push_back(handleCsv(csv));
                txn.exec0(curr_db.back().initTable());
                txn.exec0(curr_db.back().insertData());
            }

            txn.commit();
        }
    } catch(const std::exception& e) {
        std::cout << "Error: " << e.what() << std::endl;
    }
}

std::vector<std::string> findAllCsvs(const std::string& path) {
    std::vector<std::string> all_paths; // Storing all needed paths

    // Entry is each path that is in the given directory path
    for(const auto& entry : file_sys::recursive_directory_iterator(path)) {
        // Check if the given path is not for the directory, and is a file with extension .csv
        if(entry.is_regular_file() && (entry.path().extension().string()) == ".csv") {
            all_paths.push_back(correctPath(entry.path().string())); // Adding if it is a valid csv
        }
    }

    return all_paths;
}

std::string toLower(const std::string& line) {
    std::string lower = line;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

    return lower;
}

std::string correctPath(const std::string& path) {
    std::string correctedPath = path;
    std::replace(correctedPath.begin(), correctedPath.end(), '\\', '/');

    return correctedPath;
}

Sql_table handleCsv(const std::string& path) {
    std::ifstream csv(path); // opening the csv file

    std::string line;
    std::getline(csv, line);
    std::vector<std::string> headers = fetchLine(line); // Saving headers

    // Saving values
    std::vector<std::vector<std::string>> values;
    while(std::getline(csv, line)) {
        values.push_back(fetchLine(line));
    }

    size_t last_slash = path.rfind('/');
    size_t last_dot = path.rfind('.');

    std::string table_name;

    if(last_slash != std::string::npos && last_dot != std::string::npos && last_slash + 1 < last_dot) 
        table_name = path.substr(last_slash + 1, last_dot - last_slash - 1);
    else table_name = "table";

    Sql_table table(table_name, headers, values); // Creating new table

    return table;
}

std::vector<std::string> fetchLine(const std::string& line) {
    std::stringstream ss_line(line);
    std::vector<std::string> row;
    std::string val;

    while(std::getline(ss_line, val, ',')) {
        row.push_back(val);
    }
    
    return row;
}