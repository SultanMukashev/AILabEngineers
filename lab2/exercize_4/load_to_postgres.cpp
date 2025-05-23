#include <pqxx/pqxx>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>

/**
 * @brief turns a read line from csv into broken down values
 * 
 * @param line a line to be broken down
 * @return std::vector<std::string> of values for the table
 */
std::vector<std::string> rowReader(const std::string& line);

int main() {
    try {
        pqxx::connection conn("host=localhost port=5433 user=user password=password dbname=mydb");

        if(conn.is_open()) {
            pqxx::work txn(conn); // Create transaction to store queries

            std::ifstream csv("../data/result.csv"); // Open csv
            std::string line;

            if(csv.is_open()) {
                std::getline(csv, line); // Skip the first line

                while(std::getline(csv, line)) {
                    std::vector<std::string> row = rowReader(line);

                    std::string date = row[11].substr(0, 10); // Read the date part

                    // Create Query to write into the table
                    txn.exec(
                        pqxx::zview("INSERT INTO test_table(fall,geolocation_0,geolocation_1,geolocation_type,id,mass,name,nametype,recclass,reclat,reclong,year) VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, TO_DATE($12, 'YYYY-MM-DD'))"),
                        pqxx::params(row[0], std::stod(row[1]), std::stod(row[2]), row[3], std::stoi(row[4]), std::stoi(row[5]), row[6], row[7], row[8], std::stod(row[9]), std::stod(row[10]), date)
                    );
                }
            }
            txn.commit(); // Commit changes
        }
    } catch(const std::exception& e) {
        std::cerr << "Error: " << e.what();
        return 1;
    }

    return 0;
}

std::vector<std::string> rowReader(const std::string& line) {
    std::stringstream ss_line(line);
    std::vector<std::string> row;
    std::string val;

    // Break down values by commas
    while(std::getline(ss_line, val, ',')) {
        if (!val.empty() && val.front() == '"' && val.back() == '"') {
            val = val.substr(1, val.size() - 2);
        }

        row.push_back(val);
    }

    return row;
}