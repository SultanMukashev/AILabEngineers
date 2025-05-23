#ifndef SQLTYPE_H
#define SQLTYPE_H

#include <iostream>
#include <variant>
#include <string>
#include <type_traits>

namespace SqlType {
    struct NoType {}; // Undefined type
    struct BOOLEAN {}; // Boolean type

    // Simple numeric types
    namespace Numeric {
        enum class Type {
            TINYINT,
            SMALLINT,
            INTEGER,
            BIGINT,
            FLOAT,
            DOUBLE
        };

        struct NumericInfo {
            Numeric::Type type;
            bool is_unsigned = true;
        
            NumericInfo(Numeric::Type t, bool u = true, int p = 0, int s = 0)
                : type(t), is_unsigned(u) {}
            
            SqlType::Numeric::Type getType() const { return this->type; }
            void setType(SqlType::Numeric::Type type) { this->type = type; }
        };
    }

    // Sql string type and it's info stored as length
    namespace Sql_String {
        enum class Type {
            CHAR,
            TEXT,
            VARCHAR
        };

        struct Sql_StringInfo {
            Type type;
            size_t len;

            Sql_StringInfo(Type t, size_t len = 0)
                : type(t), len(len) {}

            SqlType::Sql_String::Type getType() const { return this->type; }
            void setType(SqlType::Sql_String::Type type) { this->type = type; }
        };
    }

    // Sql date type
    namespace DateTime {
        enum class Type {
            DATE,
            TIME,
            TIMESTAMP
        };

        struct DateTimeInfo {
            DateTime::Type type;
            bool with_timezone = false;
        
            DateTimeInfo(DateTime::Type t, bool tz = false)
                : type(t), with_timezone(tz) {}
            
            SqlType::DateTime::Type getType() const { return this->type; }
            void setType(SqlType::DateTime::Type type) { this->type = type; }
        };
    }

    using SqlDataType = std::variant<
        NoType,
        BOOLEAN,
        Numeric::NumericInfo,
        Sql_String::Sql_StringInfo,
        DateTime::DateTimeInfo
    >;

    std::string toString(const SqlDataType& type);
}

#endif