#include "Sql_table.h"

Sql_table::Sql_table(const std::string& name,
    const std::vector<std::string>& headers,
    const std::vector<std::vector<std::string>>& values)
: name(name), headers(headers), values(values) {}

bool Sql_table::isBoolean(const std::string& val) {
    std::string temp;
    std::transform(val.begin(), val.end(), std::back_inserter(temp), ::tolower);

    return temp == "true" || temp == "false" || temp =="null";
}
SqlType::SqlDataType Sql_table::toDateTime(const std::string& val) {
    std::tm tm = {};

    // Match TIMESTAMP
    if (std::regex_match(val, std::regex(R"(^\d{4}[-/]\d{2}[-/]\d{2} \d{2}:\d{2}:\d{2}$)"))) {
        std::istringstream ss(val);
        ss >> std::get_time(&tm, "%Y-%m-%d %H:%M:%S");
        if (ss.fail()) {
            ss.clear(); ss.str(val);
            ss >> std::get_time(&tm, "%Y/%m/%d %H:%M:%S");
        }
        if (!ss.fail()) {
            return SqlType::DateTime::DateTimeInfo{SqlType::DateTime::Type::TIMESTAMP};
        }
    }

    // Match DATE only
    if (std::regex_match(val, std::regex(R"(^\d{4}[-/]\d{2}[-/]\d{2}$)"))) {
        std::istringstream ss(val);
        ss >> std::get_time(&tm, "%Y-%m-%d");
        if (ss.fail()) {
            ss.clear(); ss.str(val);
            ss >> std::get_time(&tm, "%Y/%m/%d");
        }
        if (!ss.fail()) {
            return SqlType::DateTime::DateTimeInfo{SqlType::DateTime::Type::DATE};
        }
    }

    // Match TIME only
    if (std::regex_match(val, std::regex(R"(^\d{2}:\d{2}:\d{2}$)"))) {
        std::istringstream ss(val);
        ss >> std::get_time(&tm, "%H:%M:%S");
        if (!ss.fail()) {
            return SqlType::DateTime::DateTimeInfo{SqlType::DateTime::Type::TIME};
        }
    }

    return SqlType::NoType{};
}
SqlType::SqlDataType Sql_table::toNumeric(const std::string& val) {
    if (!val.empty() && val[0] == '0') {
        return SqlType::NoType{};
    }

    if(!val.empty() && !std::isdigit(val[0]) && val[0] != '-') {
        return SqlType::NoType{};
    }

    bool has_dot = false;

    for(size_t i = 1; i < val.length(); i++) {
        if(val[i] == '.') {
            if(!has_dot) has_dot = true;
            else return SqlType::NoType{};
        }
        if(!std::isdigit(val[i]) && val[i] != '.') return SqlType::NoType{};
    }
    long long num;
    auto res_1 = std::from_chars(val.data(), val.data() + val.size(), num); 

    if(res_1.ec == std::errc()) {
        if(std::numeric_limits<int16_t>::lowest() <= num &&
        std::numeric_limits<int16_t>::max() >= num) {
            return SqlType::Numeric::NumericInfo {
                SqlType::Numeric::Type::SMALLINT,
                num < 0 ? false : true
            };
        }
        else if(std::numeric_limits<int32_t>::lowest() <= num &&
        std::numeric_limits<int32_t>::max() >= num) {
            return SqlType::Numeric::NumericInfo {
                SqlType::Numeric::Type::INTEGER,
                num < 0 ? false : true
            };
        } else {
            return SqlType::Numeric::NumericInfo {
                SqlType::Numeric::Type::BIGINT,
                num < 0 ? false : true
            };
        }
    }

    float f_num;
    auto res_2 = std::from_chars(val.data(), val.data() + val.size(), f_num);

    if(res_2.ec == std::errc()) {
        return SqlType::Numeric::NumericInfo {
            SqlType::Numeric::Type::FLOAT,
            f_num < 0 ? false : true
        };
    }

    double d_num;
    auto res_3 = std::from_chars(val.data(), val.data() + val.size(), d_num);

    if(res_3.ec == std::errc()) {
        return SqlType::Numeric::NumericInfo {
            SqlType::Numeric::Type::DOUBLE,
            d_num < 0 ? false : true
        };
    }

    return SqlType::NoType{};
}

SqlType::SqlDataType Sql_table::processDataType(const std::string& val, size_t& max_len) {

    max_len = std::max(max_len, val.length());

    if(this->isBoolean(val)) {
        return SqlType::BOOLEAN{};
    }
    auto date = this->toDateTime(val);
    if(!std::holds_alternative<SqlType::NoType>(date)) {
        return date;
    }
    auto num = this->toNumeric(val);
    if(!std::holds_alternative<SqlType::NoType>(num)) {
        return num;
    }

    return SqlType::Sql_String::Sql_StringInfo {
        SqlType::Sql_String::Type::CHAR,
        val.length()
    };
}

int Sql_table::dataTypePriority(const SqlType::SqlDataType& type) {
    if(std::holds_alternative<SqlType::NoType>(type)) return -1;
    else if(std::holds_alternative<SqlType::Sql_String::Sql_StringInfo>(type)) return 2;
    else return 1;
}

std::string Sql_table::getName() { return this->name; }

std::string Sql_table::initTable() {
    // 1) Infer column types & track max length per column
    col_datatypes.resize(headers.size(), SqlType::NoType{});
    std::vector<size_t> max_lens(headers.size(), 0);

    for (size_t r = 0; r < values.size(); ++r) {
        for (size_t c = 0; c < headers.size(); ++c) {
            SqlType::SqlDataType curr_type =
                processDataType(values[r][c], max_lens[c]);

            // upgrade type if this row demands a “wider” type
            if (dataTypePriority(col_datatypes[c]) < dataTypePriority(curr_type)) {
                col_datatypes[c] = curr_type;
            }
            // if same priority but different type, switch to VARCHAR/TEXT
            else if (dataTypePriority(col_datatypes[c]) == dataTypePriority(curr_type) &&
                    SqlType::toString(col_datatypes[c]) != SqlType::toString(curr_type)) {
                if (max_lens[c] <= 255) {
                    col_datatypes[c] = SqlType::Sql_String::Sql_StringInfo{
                        SqlType::Sql_String::Type::VARCHAR,
                        max_lens[c]
                    };
                } else {
                    col_datatypes[c] = SqlType::Sql_String::Sql_StringInfo{
                        SqlType::Sql_String::Type::TEXT,
                        max_lens[c]
                    };
                }
            }
        }
    }

    // 2) Find the first column whose values are all unique
    int PK_col = -1;
    for (size_t c = 0; c < headers.size(); ++c) {
        std::set<std::string> seen;
        bool all_unique = true;

        for (auto &row : values) {
            if (seen.count(row[c])) {
                all_unique = false;
                break;
            }
            seen.insert(row[c]);
        }

        if (all_unique) {
            PK_col = static_cast<int>(c);
            break;
        }
    }

    // 3) Build the CREATE TABLE statement
    std::string exec_command = "CREATE TABLE IF NOT EXISTS \"" + name + "\" (";

    for (size_t c = 0; c < headers.size(); ++c) {
        // column name + its inferred SQL type
        exec_command +=
            "\"" + headers[c] + "\" " +
            SqlType::toString(col_datatypes[c]);

        // mark primary key
        if (static_cast<int>(c) == PK_col) {
            exec_command += " PRIMARY KEY";
        }

        // comma between columns
        if (c + 1 < headers.size()) {
            exec_command += ", ";
        }
    }

    exec_command += ");";

    return exec_command;
}

std::string Sql_table::correctToType(const std::string& val, const SqlType::SqlDataType& type) {
    if (val.empty() || val == "null" || val == "NULL") {
        return "NULL";
    }

    // Strings and date/time types need quotes and escaping
    if (std::holds_alternative<SqlType::Sql_String::Sql_StringInfo>(type) ||
        std::holds_alternative<SqlType::DateTime::DateTimeInfo>(type)) {
        
        std::string escaped = val;
        size_t pos = 0;
        while ((pos = escaped.find('\'', pos)) != std::string::npos) {
            escaped.insert(pos, "'");
            pos += 2;
        }
        return "'" + escaped + "'";
    }

    // Boolean type
    if (std::holds_alternative<SqlType::BOOLEAN>(type)) {
        std::string lowered = val;
        return (lowered == "true") ? "TRUE" : "FALSE";
    }

    // Numeric types: return as-is (assumes already validated)
    return val;
}

std::string Sql_table::insertData() {
    if(values.empty()) return "";
    std::string exec_command = "INSERT INTO \"" + name + "\" (";

    for (size_t i = 0; i < headers.size(); ++i) {
        exec_command += "\"" + headers[i] + "\"";
        if (i + 1 < headers.size()) exec_command += ", ";
    }
    exec_command += ") VALUES ";

    for (size_t r = 0; r < values.size(); ++r) {
        const auto& row = values[r];

        exec_command += "(";
        for (size_t i = 0; i < row.size(); i++) {
            exec_command += this->correctToType(row[i], col_datatypes[i]);
            if (i + 1 < row.size()) exec_command += ", ";
        }
        exec_command += ")";

        // Add comma between rows, except for the last one
        if (r + 1 < values.size()) exec_command += ", ";
    }
    exec_command += ";";
    
    return exec_command;
}