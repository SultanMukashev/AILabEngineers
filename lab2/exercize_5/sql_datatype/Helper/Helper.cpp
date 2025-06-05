#include "./Helper.h"
#include <regex>

SqlType::SqlType Sql_Utils::convertToType(const std::string& val) {
    SqlType::SqlType res;
    res.length = val.length();

    SqlType::SqlType temp = toBoolean(val);
    if(res.type == SqlType::BaseType::UNDEFINED) res.type = temp.type;

    temp = toNumeric(val);
    res.is_unsigned = temp.is_unsigned;
    if(res.type == SqlType::BaseType::UNDEFINED) res.type = temp.type;

    temp = toDateTime(val);
    res.with_timezone = temp.with_timezone;
    if(res.type == SqlType::BaseType::UNDEFINED) res.type = temp.type;

    temp = toTextual(val);
    res.length = val.length();
    if(res.type == SqlType::BaseType::UNDEFINED) res.type = temp.type;

    return res;
}

SqlType::SqlType Sql_Utils::merge(const SqlType::SqlType& prev, const SqlType::SqlType& curr) {
    SqlType::SqlType res;
    res.type = (getPriority(prev.type) > getPriority(curr.type))? prev.type : curr.type;
    res.length = std::max(curr.length, prev.length);
    res.is_unsigned = curr.is_unsigned && prev.is_unsigned;
    res.with_timezone = curr.with_timezone || prev.with_timezone;

    return res;
}

int Sql_Utils::getPriority(const SqlType::BaseType& t) {
    return priority_map[static_cast<int>(t)];
}

SqlType::SqlType Sql_Utils::toNumeric(const std::string& val) {
    SqlType::SqlType res;

    try {
        std::size_t pos;
        double num = std::stod(val, &pos);

        if(pos != val.length()) return res;

        res.is_unsigned = (num >= 0);

        if(std::floor(num) == num) {
            long long int_num = static_cast<long long>(num);

            if(int_num >= INT16_MIN &&int_num <= INT16_MAX) res.type = SqlType::BaseType::SMALLINT;
            else if(int_num >= INT32_MIN && int_num <= INT32_MAX) res.type = SqlType::BaseType::INTEGER;
            else res.type = SqlType::BaseType::BIGINT;
        } else {
            res.type = SqlType::BaseType::DOUBLE;
        }

        return res;
    } catch(const std::exception&) {
        return {};
    }
}

SqlType::SqlType Sql_Utils::toTextual(const std::string& val) {
    SqlType::SqlType res;
    res.type = SqlType::BaseType::CHAR;
    res.length = val.length();

    if (val.length() <= 10) res.type = SqlType::BaseType::CHAR;
    else if (val.length() <= 255) res.type = SqlType::BaseType::VARCHAR;
    else res.type = SqlType::BaseType::TEXT;

    return res;
}

SqlType::SqlType Sql_Utils::toBoolean(const std::string& val) {
    SqlType::SqlType res;

    std::string temp = val;
    std::transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
    if(temp == "true" || temp == "false" || temp == "null") res.type = SqlType::BaseType::BOOLEAN;
    else res = SqlType::SqlType{};

    return res;
}

SqlType::SqlType Sql_Utils::toDateTime(const std::string& val) {
    SqlType::SqlType res;

    // ISO Date: YYYY-MM-DD
    static const std::regex date_regex(R"(^\d{4}[-/]\d{2}[-/]\d{2}$)");

    // ISO Time: HH:MM[:SS]
    static const std::regex time_regex(R"(^\d{2}:\d{2}(:\d{2})?$)");

    // ISO Timestamp: YYYY-MM-DD[T ]HH:MM[:SS]
    static const std::regex timestamp_regex(R"(^\d{4}[-/]\d{2}[-/]\d{2}[ T]\d{2}:\d{2}(:\d{2})?$)");

    if (std::regex_match(val, timestamp_regex)) {
        res.type = SqlType::BaseType::TIMESTAMP;
    } else if (std::regex_match(val, date_regex)) {
        res.type = SqlType::BaseType::DATE;
    } else if (std::regex_match(val, time_regex)) {
        res.type = SqlType::BaseType::TIME;
    } else {
        res = SqlType::SqlType{};
    }

    return res;
}