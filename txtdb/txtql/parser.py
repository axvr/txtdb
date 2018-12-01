from collections import namedtuple

StringNode = namedtuple("StringNode", "value")
IntegerNode = namedtuple("IntegerNode", "value")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        pass

    def __parse_string(self):
        return StringNode(value=self.__consume().value)

    def __parse_integer(self):
        return IntegerNode(value=self.__consume().value)

    def __consume(self, expected_type):
        token = self.tokens.pop(0)

        if token.type == expected_type:
            return token
        else:
            raise RuntimeError("Expected token type \"" + expected_type +
                    "\", but got \"" + token.type + "\"")

    def __peek(self, expected_type, offset=0):
        return self.tokens[offset].type == expected_type
