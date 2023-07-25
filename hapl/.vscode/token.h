#ifndef TOKEN_H
#define TOKEN_H

#include <string>

class Token {
    /* 
    Token class for lexing.
    */
public:
    std::string type;
    std::string value;

    Token(std::string type, std::string value);
    std::string getTokenValue();
};

#endif  // TOKEN_H