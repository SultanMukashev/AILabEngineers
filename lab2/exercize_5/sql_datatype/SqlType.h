#ifndef SQLTYPE_H
#define SQLTYPE_H

#include <iostream>
#include <string>

namespace SqlType {

enum class BaseType {
    UNDEFINED,
    BOOLEAN,
    TIMESTAMP,
    TIME,
    DATE,
    SMALLINT,
    INTEGER,
    BIGINT,
    FLOAT,
    DOUBLE,
    CHAR,
    VARCHAR,
    TEXT
};

struct SqlType {
    BaseType type = BaseType::UNDEFINED;
    std::size_t length = 0;           // For CHAR, VARCHAR
    bool is_unsigned = true;  // For numeric types
    bool with_timezone = false; // For TIMESTAMP, TIME
};

std::string toString(const SqlType& t);
}

#endif