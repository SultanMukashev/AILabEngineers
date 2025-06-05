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
#include "../sql_datatype/Helper/Helper.h"

class Sql_table {
private:
    std::string name;
    std::vector<SqlType::SqlType> col_datatypes;

    std::vector<std::string> headers;
    std::vector<std::vector<std::string>> values;

    Sql_Utils sqlu;
public:
    Sql_table(const std::string& name,
        const std::vector<std::string>& headers,
        const std::vector<std::vector<std::string>>& values);
    std::string getName();

    std::string initTable();
    std::string insertData();
};

#endif