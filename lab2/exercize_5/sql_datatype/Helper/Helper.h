#ifndef SQLUTILS_H
#define SQLUTILS_H

#include <iostream>
#include <string>
#include <algorithm>
#include <math.h>

#include "../SqlType.h"

constexpr int priority_map[static_cast<int>(SqlType::BaseType::TEXT) + 1] = {
    0,  // UNDEFINED
    1,  // BOOLEAN
    2,  // TIMESTAMP
    3,  // TIME
    4,  // DATE
    5,  // SMALLINT
    6,  // INTEGER
    7,  // BIGINT
    8,  // FLOAT
    9,  // DOUBLE
    10, // CHAR
    11, // VARCHAR
    12  // TEXT
};

class Sql_Utils {
public:
    SqlType::SqlType toNumeric(const std::string& val);
    SqlType::SqlType toTextual(const std::string& val);
    SqlType::SqlType toBoolean(const std::string& val);
    SqlType::SqlType toDateTime(const std::string& val);

    SqlType::SqlType convertToType(const std::string& val);
    SqlType::SqlType merge(const SqlType::SqlType& prev_type, const SqlType::SqlType& curr_type);
    int getPriority(const SqlType::BaseType& t);
};

#endif