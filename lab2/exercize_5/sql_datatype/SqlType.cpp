#include "SqlType.h"

namespace SqlType {
  std::string toString(const SqlType& t) {
    switch (t.type) {
        case BaseType::BOOLEAN:   return "BOOLEAN";
        case BaseType::SMALLINT:  return "SMALLINT";
        case BaseType::INTEGER:   return "INTEGER";
        case BaseType::FLOAT:     return "FLOAT";
        case BaseType::DOUBLE:    return "DOUBLE";
        case BaseType::CHAR:      return "CHAR(" + std::to_string(t.length) + ")";
        case BaseType::VARCHAR:   return "VARCHAR(" + std::to_string(t.length) + ")";
        case BaseType::TEXT:      return "TEXT";
        case BaseType::DATE:      return "DATE";
        case BaseType::TIME:      return "TIME";
        case BaseType::TIMESTAMP: return "TIMESTAMP";
        default:              return "UNDEFINED";
    }
  }
}