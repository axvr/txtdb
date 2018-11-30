import re

class Tokenizer:
    TOKEN_TYPES = [
        ["select", "\\bSELECT\\b"],
        ["where",  "\\bWHERE\\b"],
        ["from",   "\\bFROM\\b"],
        ["order",  "\\bORDER\\s+BY\\b"],
        ["create", "\\bCREATE\\b"],
        ["drop",   "\\bDROP\\b"],
        ["table",  "\\bTABLE\\b"],
        ["name", "\\b(?:[a-zA-Z]+|\\[[a-zA-Z _-]+\\])\\b"],
        ["string", "'.*?(?<!\\\)'"],
        ["comma", ","],
        ["integer", "\\b[0-9]+\\b"],
        ["and", "\\bAND\\b"],
        ["or", "\\bOR\\b"],
        ["not", "\\bNOT\\b"],
        ["notequal", "(?:!=|<>)"],
        ["equal", "="],
        ["plus", "\\+"],
        ["subtract", "-"],
        ["multiply", "\\*"],
        ["divide", "\\/"],
        ["modulo", "%"]
    ]

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []

        self.code = self.code.strip()

        while self.code != "":
            tokens.append(self.tokenize_one_token())
            self.code = self.code.strip()
            print(str(tokens))

        return tokens

    def tokenize_one_token(self):
        for (type, pattern) in self.TOKEN_TYPES:
            m = re.match("\\A(" + pattern + ")", self.code, re.IGNORECASE)
            if m is not None:
                value = m.group(1)
                self.code = self.code[len(value):]
                return (type, value)

        raise RuntimeError("Couldn't match a token on \"" +
                self.code + "\"")
