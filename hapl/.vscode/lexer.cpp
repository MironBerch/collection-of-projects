#include <iostream>
#include "token.h"

int main() {
    Token token("Identifier", "x");
    std::string tokenValue = token.getTokenValue();

    std::cout << "Token Value: " << tokenValue << std::endl;

    return 0;
}