import re
from collections import namedtuple

Token = namedtuple('Token', 'type value')

class Tokeniser:
    # TODO add more tokens
    TOKEN_TYPES = [
        ["comment", r"/\*.*?\*/"],
        ["select", r"(?i)\bSELECT\b"],
        ["where", r"(?i)\bWHERE\b"],
        ["insert", r"(?i)\bINSERT\b"],
        ["update", r"(?i)\bUPDATE\b"],
        ["delete", r"(?i)\bDELETE\b"],
        ["truncate", r"(?i)\bTRUNCATE\b"],
        ["into", r"(?i)\bINTO\b"],
        ["from", r"(?i)\bFROM\b"],
        ["values", r"(?i)\bVALUES\b"],
        ["order", r"(?i)\bORDER\s+BY\b"],
        ["group", r"(?i)\bGROUP\s+BY\b"],
        ["create", r"(?i)\bCREATE\b"],
        ["join_left_outer", r"(?i)\bLEFT\s+(?:OUTER\s+)?JOIN\b"],
        ["join_right_outer", r"(?i)\bRIGHT\s+(?:OUTER\s+)?JOIN\b"],
        ["join_full_outer", r"(?i)\bFULL\s+(?:OUTER\s+)?JOIN\b"],
        ["join_cross", r"(?i)\bCROSS\s+JOIN\b"],
        ["join_inner", r"(?i)\b(?:INNER\s+)?JOIN\b"],
        ["set", r"(?i)\bSET\b"],
        ["on", r"(?i)\bON\b"],
        ["in", r"(?i)\bIN\b"],
        ["as", r"(?i)\bAS\b"],
        ["exists", r"(?i)\bEXISTS\b"],
        ["drop", r"(?i)\bDROP\b"],
        ["table", r"(?i)\bTABLE\b"],
        ["asterisk", r"\*"],
        ["comma", r","],
        ["integer", r"\b[0-9]+\b"],
        ["true", r"(?i)\bTRUE\b"],
        ["false", r"(?i)\bFALSE\b"],
        ["null", r"(?i)\bNULL\b"],
        ["and", r"(?i)\bAND\b"],
        ["or", r"(?i)\bOR\b"],
        ["not", r"(?i)\bNOT\b"],
        ["not_equal", r"(?:!=|<>)"],
        ["add", r"\+"],
        ["subtract", r"-"],
        ["divide", r"/"],
        ["modulo", r"%"],
        ["greater", r">"],
        ["less", r"<"],
        ["greater_equal", r">="],
        ["less_equal", r"<="],
        ["equal", r"="],
        ["name", r"(?:\b[a-zA-Z]+\b|\[[a-zA-Z _.-]+\])"],
        ["string", r"'.*?(?<!\\)'"],
        ["open_paren", r"\("],
        ["close_paren", r"\)"],
    ]

    def __init__(self, code):
        self.code = code

    def tokenise(self):
        tokens = []

        self.code = self.code.strip()

        while self.code != "":
            tokens.append(self.__tokenise_next_token())
            self.code = self.code.strip()

        return tokens

    def __tokenise_next_token(self):
        for (type, pattern) in self.TOKEN_TYPES:
            m = re.match(r"\A(" + pattern + r")", self.code)
            if m is not None:
                value = m.group(1)
                self.code = self.code[len(value):]
                return Token(type=type, value=value)

        raise RuntimeError("Couldn't match a token on \"" +
                self.code + "\"")
