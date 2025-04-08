#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <pqxx/pqxx>

using DB_row_t = std::vector<std::string>; // Defining for easier access of the value

DB_row_t rowReader(const std::string &line); // Reading rows of the CSV file

int main() {
    try {
        pqxx::connection conn("host=localhost port=5433 user=user password=password dbname=mydb");

        if(conn.is_open()) {
            std::cout << "Connected to " << conn.dbname() << std::endl;

            pqxx::work txn(conn); // Creating transaction to work with db

            std::ifstream studets_CSV; // CSV and reading it
            std::string line = "";

            studets_CSV.open("../data/students.csv");

            if(studets_CSV.is_open()) {
                std::getline(studets_CSV, line);
                while(std::getline(studets_CSV, line)) {
                    DB_row_t row = rowReader(line);

                    // pqxx::zview - the command
                    // pqxx::params - values passwed into the table
                    txn.exec(
                        pqxx::zview("INSERT INTO students(id, full_name, gpa, email) VALUES($1, $2, $3, $4)"),
                        pqxx::params(std::stoi(row[0]), row[1], std::stod(row[2]), row[3])
                    );
                }

                txn.commit(); // Commiting changes
            } else {
                std::cout << "Students.csv is not open" << std::endl;
            }
        } else {
            std::cout << "Error while connecting";
        }
    } catch (const std::exception &e) {
        std::cerr << "Connection error: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}

DB_row_t rowReader(const std::string &line) {
    std::stringstream ss_line(line);
    std::string val = ""; // single value of the row
    DB_row_t row; // Row value broken down as each value

    while(std::getline(ss_line, val, ',')) {
        row.push_back(val); // Pushing each value after breaking each line of the CSV by commas
    }

    return row;
}