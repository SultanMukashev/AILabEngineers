#include "SqlType.h"

std::string SqlType::toString(const SqlDataType& v) {
  return std::visit([](const auto& t) -> std::string {
    using T = std::decay_t<decltype(t)>;

    if constexpr (std::is_same_v<T, NoType>) {
      return "UNDEFINED";
    }
    else if constexpr (std::is_same_v<T, BOOLEAN>) {
      return "BOOLEAN";
    }
    else if constexpr (std::is_same_v<T, Numeric::NumericInfo>) {
      switch (t.getType()) {
        case Numeric::Type::TINYINT:   return "TINYINT";
        case Numeric::Type::SMALLINT:  return "SMALLINT";
        case Numeric::Type::INTEGER:   return "INTEGER";
        case Numeric::Type::BIGINT:    return "BIGINT";
        case Numeric::Type::FLOAT:     return "FLOAT";
        case Numeric::Type::DOUBLE:    return "DOUBLE";
      }
      return "NUMERIC";  // catch‑all for NumericInfo
    }
    else if constexpr (std::is_same_v<T, Sql_String::Sql_StringInfo>) {
      switch (t.getType()) {
        case Sql_String::Type::CHAR:    return "CHAR(" + std::to_string(t.len) + ")";
        case Sql_String::Type::TEXT:    return "TEXT";
        case Sql_String::Type::VARCHAR: return "VARCHAR(" + std::to_string(t.len) + ")";
      }
      return "STRING";
    }
    else if constexpr (std::is_same_v<T, DateTime::DateTimeInfo>) {
      switch(t.getType()) {
        case DateTime::Type::TIME:      return "TIME";
        case DateTime::Type::TIMESTAMP: return "TIMESTAMP";
        case DateTime::Type::DATE:      return "DATE";
      }
      return "DATETIME";
    }

    // **fallback if you ever add a new variant alternative**  
    return "UNKNOWN";
  }, v);
}
