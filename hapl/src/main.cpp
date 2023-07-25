#include <iostream>
#include <string>
#include "read_code.h"

int main(int argc, char* argv[]) {
    std::string code = readCode(argv[1]);
    std::cout << argv[1] << std::endl;
    std::cout << code << std::endl;
    return 0;
}
