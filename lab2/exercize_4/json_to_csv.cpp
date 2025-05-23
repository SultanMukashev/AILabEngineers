#include <nlohmann/json.hpp>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <vector>
#include <map>

namespace file_sys = std::filesystem;

using json = nlohmann::json;

/**
 * @brief Finds all jsons in the project
 * 
 * @param path a path from where the jsons are read
 * @return An std::vector<std::string> with all file paths to the jsons
 */
std::vector<std::string> findAllJsons(const std::string& path);
/**
 * @brief turns strings to lower case
 */
std::string toLower(const std::string& str);
/**
 * @brief handles json paths work
 * 
 * @param path_to_json a path to json file to work with
 * @param csv a csv file where json will be written
 * @param headers_written if headers are written
 */
void handleJson(const std::string& path_to_json, std::ofstream& csv, bool& headers_written);
/**
 * @brief flattens a json file
 * 
 * @param j the json file to be flatten, recursed for objects and arrays
 * @param out a map where the flattened result will be written in
 * @param prefix the prefix of flattened value(for the key)
 */
void flattenJson(const json& j, std::map<std::string, std::string>& out, const std::string& prefix = "");

int main() {
    std::vector<std::string> json_paths = findAllJsons("./data"); // Storing all jsons from data

    std::ofstream csv("../data/result.csv"); // Path to write csv
    bool headers_written = false; // if headers are written

    // Handle each json
    for(std::string json_path : json_paths) {
        handleJson(json_path, csv, headers_written);
    }
}

std::vector<std::string> findAllJsons(const std::string& path) {
    std::vector<std::string> all_paths; // Storing all json paths here

    // iterating through each file in the given directory
    for(const auto& entry : file_sys::recursive_directory_iterator(path)) {
        // Checking if given file is regular file(not a directory or anything) and if it's extn=ension is json
        if(entry.is_regular_file() && toLower(entry.path().extension().string()) == ".json") {
            std::string path = entry.path().string();
            std::replace(path.begin(), path.end(), '\\', '/');
            all_paths.push_back(path); // Saving the path if it is json
        }
    }

    return all_paths;
}

std::string toLower(const std::string& str) {
    std::string lower = str;
    std::transform(lower.begin(), lower.end(), lower.begin(), ::tolower);

    return lower;
}

void handleJson(const std::string& path_to_json, std::ofstream& csv, bool& headers_written) {
    std::ifstream json_file(path_to_json); // Opening json as input stream of a file

    // handling if such path doesn't exist
    if(!json_file) {
        std::cerr << "Couldn't find fson file" << std::endl;
        return;
    }

    json j;
    json_file >> j; // Writing json as json object(from nlohmann)

    std::map<std::string, std::string> flat_json;

    flattenJson(j, flat_json); // Flattening json into a map and saving it

    // Writing headers if there are none
    if(!headers_written) {
        for(auto it = flat_json.begin(); it != flat_json.end(); ++it) {
            csv << it->first;

            if(std::next(it) != flat_json.end()) {
                csv << ",";
            }
        }
        csv << '\n';

        headers_written = true;
    }

    // Writing the values
    for(auto it = flat_json.begin(); it != flat_json.end(); ++it) {
        csv << it->second;

        if(std::next(it) != flat_json.end()) {
            csv << ",";
        }
    }
    csv << '\n';
}

void flattenJson(const json& j, std::map<std::string, std::string>& out, const std::string& prefix) {
    for(auto& el : j.items()) {
        std::string key = prefix; // Creating key for the values in the map

        if(!prefix.empty() && !el.key().empty()) {
            key += ".";
        }
        key += el.key();

        if(el.value().is_primitive()) {
            out[key] = el.value().dump(); // If it is a primitive type, just write key-value pair
        } else if(el.value().is_object()) {
            flattenJson(el.value(), out, key); // If an object use recursion
        } else if(el.value().is_array()) {
            // If an array, use recursion in the for loop
            for(size_t i = 0; i < el.value().size(); ++i) {
                std::string array_key = prefix.empty() ? std::to_string(i) : prefix + "." + std::to_string(i);
                flattenJson(el.value()[i], out, array_key);
            }
        }
    }
}