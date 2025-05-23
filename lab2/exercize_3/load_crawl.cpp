#include <curl/curl.h>
#include <zlib.h>
#include <iostream>
#include <vector>

struct MemoryBuffer {
    std::vector<char> data;
};

/**
 * @brief Define curl WRITEFUNCTION to write in temporary MemoryBuffer
 * 
 * @param contents contents of the data that are read
 * @param size size of each data part(normally 1 byte)
 * @param nmemb number of data parts
 * @param user_ptr pointer to user that will be used to read the data
 * @return size of the read data
 */
size_t WriteToMemory(void* contents, size_t size, size_t nmemb, void* user_ptr);
/**
 * @brief reads the content into the buffer
 * 
 * @param buffer memory where data is written into
 * @param url url from which the data will be read
 */
void ReadCurlIntoBuffer(MemoryBuffer& buffer, const std::string& url);
/**
 * @brief decomposes the first line of the gz file
 * 
 * @param compressedData the data to be decompressed
 * @return first decopressed line
 */
std::vector<std::string> decomposeFirstLine(const std::vector<char>& compressedData);

int main() {
    MemoryBuffer buffer;
    ReadCurlIntoBuffer(buffer, "https://data.commoncrawl.org/crawl-data/CC-MAIN-2025-13/wet.paths.gz");
    
    std::vector<std::string> data = decomposeFirstLine(buffer.data);
    std::string full_path = "https://data.commoncrawl.org/" + data.at(0);

    MemoryBuffer wetBuffer;
    ReadCurlIntoBuffer(wetBuffer, full_path);

    std::vector<std::string> wetLines = decomposeFirstLine(wetBuffer.data);

    for (const std::string& l : wetLines) {
        std::cout << l << std::endl;
    }
}

size_t WriteToMemory(void* contents, size_t size, size_t nmemb, void* user_ptr) {
    size_t totalSize = size * nmemb;
    auto* mem = static_cast<MemoryBuffer*>(user_ptr);
    char* incoming = static_cast<char*>(contents);
    mem->data.insert(mem->data.end(), incoming, incoming + totalSize);
    return totalSize;
}

void ReadCurlIntoBuffer(MemoryBuffer& buffer, const std::string& url) {
    CURL *curl;
    CURLcode res;

    curl_global_init(CURL_GLOBAL_ALL);
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteToMemory);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

        curl_easy_perform(curl);
        curl_easy_cleanup(curl);
    }

    curl_global_cleanup();
}

std::vector<std::string> decomposeFirstLine(const std::vector<char>& compressedData) {
    z_stream strm = {};

    strm.next_in = reinterpret_cast<Bytef*>(const_cast<char*>(compressedData.data()));
    strm.avail_in = static_cast<uInt>(compressedData.size());

    inflateInit2(&strm, 16 + MAX_WBITS);

    std::vector<std::string> lines;
    std::string line;
    char out[1];

    while(true) {
        strm.next_out = reinterpret_cast<Bytef*>(out);
        strm.avail_out = 1;

        int ret = inflate(&strm, Z_NO_FLUSH);

        if (ret == Z_STREAM_END || ret == Z_BUF_ERROR) break;
        if (ret != Z_OK) {
            std::cerr << "Decompression failed!\n";
            break;
        }

        if (out[0] == '\n') {
            lines.push_back(line);
            line.clear();
        }
        line += out[0];
    }

    if(!line.empty()) lines.push_back(line);

    inflateEnd(&strm);
    return lines;
}