#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <vector>
#include <pqxx/pqxx>

// Defining that we can use values of db instead of long vector<string>
using dbRow_t = std::vector<std::string>;

// Needed to split each row of the database into values
dbRow_t splitRow(std::string const &line);

int main() {
    try {
        // Creating connection to the PostgreSQL
        pqxx::connection conn("host=postgres port=5432 dbname=mydb user=user password=password");

        if(conn.is_open()) {
            std::cout << "Connected to database: " << conn.dbname() << std::endl;
            pqxx::work txn(conn); // Starting transaction

            // Creating file stream to read from a file and a line that will store the lines
            std::ifstream data_CSV;
            std::string line = "";

            data_CSV.open("data/students.csv");
            std::getline(data_CSV, line); // Skipping first line

            while(data_CSV.is_open()) {
                while (std::getline(data_CSV, line)) {
                    dbRow_t row = splitRow(line);
                    if (row.size() >= 4) {
                        txn.exec_params(
                            "INSERT INTO students (id, full_name, gpa, email) VALUES ($1, $2, $3, $4);",
                            std::stoi(row[0]), row[1], std::stod(row[2]), row[3]
                        ); // Adding values to the transaction to database
                    }
                }
                txn.commit(); // Commiting changes
                data_CSV.close(); // Closing the file reader
            }
        } else {
            std::cerr << "Failed to connect to database." << std::endl;
            return 1;
        }
    } catch(const std::exception &e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

dbRow_t splitRow(std::string const &line) {
    std::string val = ""; // Single value that will be stored into row array
    dbRow_t row; // Row that will be returned as an answer
    std::stringstream ss(line); // String stream that will be converted into values

    while(std::getline(ss, val, ',')) {
        row.push_back(val);
    }

    row.push_back(val);
    return row;
}