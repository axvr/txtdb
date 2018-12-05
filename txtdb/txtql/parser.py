from collections import namedtuple

RootNode = namedtuple("RootNode", "select_node from_node where_node")

# Types
StringNode = namedtuple("StringNode", "value")
IntegerNode = namedtuple("IntegerNode", "value")
BooleanNode = namedtuple("BooleanNode", "value")

NameNode = namedtuple("NameNode", "value")

# TODO switch out 'SelectNode' for a more generic node
SelectNode = namedtuple("SelectNode", "columns")
WhereNode = namedtuple("WhereNode", "expression")
FromNode = namedtuple("FromNode", "table")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):

        select_node = None
        where_node  = None
        from_node   = None

        # Parse SELECT,
        if self.__peek("select"):
            select_node = self.__parse_select()

        # Parse FROM,
        if self.__peek("from"):
            from_node = self.__parse_from()

        # Parse WHERE
        if self.__peek("where"):
            where_node = self.__parse_where()

        # Repeat?

        return RootNode(select_node=select_node, from_node=from_node,
                where_node=where_node)

    def __consume(self, expected_type):
        token = self.tokens.pop(0)

        if token.type == expected_type:
            return token
        else:
            raise RuntimeError("Expected token type \"" + expected_type +
                    "\", but got \"" + token.type + "\"")

    def __peek(self, expected_type, offset=0):
        return self.tokens[offset].type == expected_type

    def __parse_string(self):
        string = self.__consume("string").value

        if string.startswith("'") and string.endswith("'"):
            string = string[1:-1]

        return StringNode(value=string)

    def __parse_integer(self):
        return IntegerNode(value=self.__consume("integer").value)

    def __parse_boolean(self):
        value = None

        if self.__peek("true"):
            self.__consume("true")
            value = True
        elif self.__peek("false"):
            self.__consume("false")
            value = False

        return BooleanNode(value=value)

    def __parse_name(self):
        name = self.__consume("name").value

        if name.startswith("[") and name.endswith("]"):
            name = name[1:-1]

        return NameNode(value=name)

    def __parse_select(self):
        self.__consume("select")

        columns = []

        # TODO check for 'select_star' token

        columns.append(self.__parse_name())

        while (self.__peek("comma")):
            self.__consume("comma")
            columns.append(self.__parse_name())

        return SelectNode(columns=columns)

    def __parse_from(self):
        self.__consume("from")
        table = self.__parse_name()
        return FromNode(table=table)

    def __parse_where(self):
        self.__consume("where")
        return WhereNode(expression=None)
