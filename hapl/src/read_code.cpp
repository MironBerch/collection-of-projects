#include <iostream>
#include <fstream>
#include <string>
#include "read_code.h"

std::string readCode(std::string fileName) {
    std::string fileContents;

    std::ifstream inputFile(fileName);
    if (inputFile.is_open()) {
        fileContents = std::string(
            (std::istreambuf_iterator<char>(inputFile)),
            std::istreambuf_iterator<char>()
        );
        inputFile.close();

        std::cout << fileContents << std::endl;
    } else {
        std::cout << "Failed to open the file." << std::endl;
    }

    return fileContents;
}
