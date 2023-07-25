#include "token.h"

Token::Token(std::string type, std::string value) : type(type), value(value) {}

std::string Token::getTokenValue() {
    return value;
}