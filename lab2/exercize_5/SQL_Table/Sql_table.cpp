#include "Sql_table.h"

Sql_table::Sql_table(const std::string& name,
    const std::vector<std::string>& headers,
    const std::vector<std::vector<std::string>>& values)
: name(name), headers(headers), values(values) {}

std::string Sql_table::getName() { return this->name; }

std::string Sql_table::initTable() {
    std::string exec_command = "CREATE TABLE IF NOT EXISTS \"" + this->getName() + "\" (";

    for (size_t col = 0; col < values[0].size(); ++col) {
        for (size_t row = 0; row < values.size(); ++row) {
            if (values[row][col].empty() || values[row][col] == "null") continue;
            SqlType::SqlType temp = sqlu.convertToType(values[row][col]);

            if (col_datatypes.size() <= col)
                col_datatypes.push_back(temp);
            else
                col_datatypes[col] = sqlu.merge(col_datatypes[col], temp);
        }
    }

    for(size_t i = 0; i < col_datatypes.size(); ++i) {
        exec_command += "\"" + headers[i] + "\" " + SqlType::toString(col_datatypes[i]);

        if(col_datatypes.size() - 1 > i) exec_command += ", ";
    }

    exec_command += ")";

    return exec_command;
}

std::string Sql_table::insertData() {
    std::string exec_command = "INSERT INTO \"" + getName() + "\" (";

    for (size_t i = 0; i < headers.size(); ++i) {
        exec_command += "\"" + headers[i] + "\"";
        if (i < headers.size() - 1) exec_command += ", ";
    }

    exec_command += ") VALUES\n";

    for (size_t i = 0; i < values.size(); ++i) {
        exec_command += "(";
        for (size_t j = 0; j < values[i].size(); ++j) {
            const std::string& val = values[i][j];

            // Add single quotes and escape single quotes inside value
            std::string escaped_val = "'";
            for (char c : val) {
                if (c == '\'') escaped_val += "''";
                else escaped_val += c;
            }
            escaped_val += "'";

            exec_command += escaped_val;

            if (j < values[i].size() - 1) exec_command += ", ";
        }
        exec_command += ")";
        if (i < values.size() - 1) exec_command += ",\n";
    }

    exec_command += ";";
    return exec_command;
}
