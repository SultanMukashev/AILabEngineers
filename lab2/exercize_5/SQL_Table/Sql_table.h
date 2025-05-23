#ifndef SQL_TABLE_H
#define SQL_TABLE_H

#include <vector>
#include <string>
#include <cstddef>
#include <algorithm>
#include <cctype>
#include <regex>
#include <sstream>
#include <ctime>
#include <iomanip>
#include <charconv>
#include <set>

#include "../sql_datatype/SqlType.h"

class Sql_table {
private:
    std::string name;
    std::vector<SqlType::SqlDataType> col_datatypes;

    std::vector<std::string> headers;
    std::vector<std::vector<std::string>> values;

    SqlType::SqlDataType processDataType(const std::string& val, size_t& max_len);
    int dataTypePriority(const SqlType::SqlDataType& type);

    bool isBoolean(const std::string& val);
    SqlType::SqlDataType toDateTime(const std::string& val);
    SqlType::SqlDataType toNumeric(const std::string& val);

    std::string correctToType(const std::string& val, const SqlType::SqlDataType& type);
public:
    Sql_table(const std::string& name,
        const std::vector<std::string>& headers,
        const std::vector<std::vector<std::string>>& values);
    std::string getName();

    std::string initTable();
    std::string insertData();
};

#endif