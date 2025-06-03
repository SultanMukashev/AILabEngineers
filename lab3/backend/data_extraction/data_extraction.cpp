#include <iostream>
#include <filesystem>
#include <zip.h>
#include <string>
#include <fstream>

namespace file_sys = std::filesystem;

/**
 * @brief extracts from zip to memory
 * 
 * @param archieve a pointer to zip file that is used to read the data from
 * @param entry_name a name of the entry with the needed data
 * @return a vector of characters(bytes) of needed data
 */
std::vector<char> extractEntryToMemory(zip* archieve, const std::string& entry_name);
/**
 * @brief Writes extracted data into new csv file
 * 
 * @param name name of the new extracted csv
 * @param data data that will be written into csv
 */
void transferMemoryToCsv(const std::string& name, const std::vector<char>& data);

int main() {
    file_sys::create_directories("../data_extracted");
    std::string data_folder = "../data_raw"; // Path to folder with zip file data

    for(const auto& entry : file_sys::directory_iterator(data_folder)) {
        if(entry.path().extension() == ".zip") {
            std::cout << "Found zip: ";

            // Opening zip file
            int err = 0;
            zip* archieve = zip_open(entry.path().string().c_str(), ZIP_RDONLY, &err);
            if (!archieve) {
                std::cerr << "Failed to open: " << entry.path() << std::endl;
                continue;
            }

            // Getting number of entries(files) in the zip
            zip_int64_t num_entries = zip_get_num_entries(archieve, 0);
            std::cout << "Contains: " << num_entries << " files: " << std::endl;

            for(zip_int64_t i = 0; i < num_entries; ++i) {
                const char* name = zip_get_name(archieve, i, 0);

                if(std::string(name).ends_with(".csv")) {
                    std::vector<char> buffer = extractEntryToMemory(archieve, name); // Extracting our data from zip

                    transferMemoryToCsv(name, buffer); // Writing data to new file
                }
            }

            zip_close(archieve); // Closing zip file
        }
    }
}

std::vector<char> extractEntryToMemory(zip* archieve, const std::string& entry_name) {
    // Creating zip stats, metadata
    struct zip_stat st;
    zip_stat_init(&st);

    // Testing if they are extracted
    if(zip_stat(archieve, entry_name.c_str(), 0, &st) != 0) {
        std::cerr << "    -Failed to stat entry: " << entry_name << std::endl;
        return {};
    }

    // Opening file as a pointer
    zip_file* file = zip_fopen(archieve, entry_name.c_str(), 0);
    if(!file) {
        std::cerr << "    -Filed to open entry: " << entry_name << std::endl;
        return {};
    }

    // Reading chunk of data
    std::vector<char> buffer(st.size);
    zip_int64_t bytes_read = zip_fread(file, buffer.data(), st.size);
    zip_fclose(file);

    if(bytes_read < 0) {
        std::cerr << "    -Failed to read an entry: " << entry_name << std::endl;
        return {};
    }

    return buffer; // Returning read data
}

void transferMemoryToCsv(const std::string& name, const std::vector<char>& data) {
    // Creating new csv file
    std::string base_name = name.substr(name.find_last_of("/\\") + 1); // Seperating what can be read for distinct file name and used for new files
    std::string new_file_path = "../data_extracted/" + base_name;
    std::string content(data.begin(), data.end()); // Reading the data as one string
    std::ofstream csv(new_file_path);

    if(!csv) {
        std::cerr << "Failed to open the file" << std::endl;
    } else {
        csv << content; // Writing to a new file
    }
}