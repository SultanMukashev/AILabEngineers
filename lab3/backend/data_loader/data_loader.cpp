#include <iostream>
#include <nlohmann/json.hpp>
#include <curl/curl.h>
#include <filesystem>
#include <map>
#include <fstream>

namespace file_sys = std::filesystem;
using json = nlohmann::json;

/**
 * @brief Reads kaggle config as json file and returns it's credentials as single string
 * 
 * @param kaggle_config_path path to kaggle config file
 */
std::string kaggleConfigReader(const std::string& kaggle_config_path);
/**
 * @brief Writes data from given kaggle url
 * 
 * @param credentials username and api for kaggle generated to be able to download needed data
 * @param url url of kaggle from where the data will be read
 */
void kaggleDataReader(const std::string& credentials, const std::string& url);
/**
 * @brief custom function to write kaggle data from CURL to file
 * 
 * @param ptr pointer to the beggining of the raw downloaded data
 * @param size size of the byte of raw data
 * @param nmemb number of bytes in raw data
 * @param stream stream of data
 */
size_t WriteToFile(void* ptr, size_t size, size_t nmemb, void* stream);
/**
 * @brief creates a path to a zip file that will take in raw data
 * 
 * @param url a url that will be used to base a new zip file name
 */
std::string kaggleFileNamer(const std::string& url);
/**
 * @brief extracts all datasets from given file line by line
 * 
 * @param path_to_datasets a string with path to the dataset urls text file
 */
std::vector<std::string> fetchDatasetUrls(const std::string& path_to_datasets);

int main() {
    // Path to kaggle download credentials
    std::string kaggle_config_path = "kaggle.json";

    std::string credentials = kaggleConfigReader(kaggle_config_path); // Extract credentials from kaggle.json

    std::vector<std::string> dataset_urls = fetchDatasetUrls("dataset_paths.txt");
    for(const std::string& dataset_url : dataset_urls) {
        kaggleDataReader(credentials, dataset_url); // Reading data into file using given credentials and url
    }
}

std::string kaggleConfigReader(const std::string& kaggle_config_path) {
    std::ifstream kaggle_raw_config(kaggle_config_path); // Reading credentials as a file

    // Reading kaggle config as json
    json kaggle_json_config;
    kaggle_raw_config >> kaggle_json_config;

    // Broken down kaggple credentials
    std::string username = kaggle_json_config["username"];
    std::string api_key = kaggle_json_config["key"];

    return username + ":" + api_key; // Full credentials key
}

void kaggleDataReader(const std::string& credentials, const std::string& url) {
    // Initializing CURL for reading kaggle data
    CURL* curl;
    CURLcode res;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    std::string raw_data_file = kaggleFileNamer(url); // Getting automatic path to the raw saved data files

    if (curl) {
        std::ofstream file(raw_data_file, std::ios::binary);

        // Options for CURL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_USERPWD, credentials.c_str()); // Basic Auth
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteToFile);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &file);
        curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1L);

        res = curl_easy_perform(curl); // Result
        if (res != CURLE_OK) {
            std::cerr << "Curl failed: " << curl_easy_strerror(res) << std::endl;
        } else {
            std::cout << "Downloaded successfully." << std::endl;
        }

        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
}

size_t WriteToFile(void* ptr, size_t size, size_t nmemb, void* stream) {
    std::ofstream* out = static_cast<std::ofstream*>(stream);
    size_t totalSize = size * nmemb;
    out->write(static_cast<char*>(ptr), totalSize);
    return totalSize;
}

std::string kaggleFileNamer(const std::string& url) {
    // Finding last slash
    size_t lastSlash = url.rfind("/");
    if (lastSlash == std::string::npos) return "../data_raw/invalid.zip";

    std::string dataset_name = url.substr(lastSlash + 1); // Extracting dataset name, end of url

    std::string raw_data_file = "../data_raw/" + dataset_name + ".zip";
    return raw_data_file;
}

std::vector<std::string> fetchDatasetUrls(const std::string& path_to_datasets) {
    std::ifstream dataset_urls(path_to_datasets); // Reading all dataset urls

    // Used to read all datasets as seperate lines
    std::string dataset;
    std::vector<std::string> all_datasets;

    while(std::getline(dataset_urls, dataset)) {
        all_datasets.push_back(dataset);
    }

    return all_datasets;
}