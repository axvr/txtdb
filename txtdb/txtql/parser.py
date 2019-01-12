from collections import namedtuple

# Types
StringNode = namedtuple("StringNode", "value")
IntegerNode = namedtuple("IntegerNode", "value")
BooleanNode = namedtuple("BooleanNode", "value")
NullNode = namedtuple("NullNode", "value")

NameNode = namedtuple("NameNode", "value")

WhereNode = namedtuple("WhereNode", "column operation value") # FIXME
FromNode = namedtuple("FromNode", "table")
SetNode = namedtuple("SetNode", "column value")

SelectNode = namedtuple("SelectNode", "columns From Where")
CreateNode = namedtuple("CreateNode", "") # TODO
InsertNode = namedtuple("InsertNode", "") # TODO
UpdateNode = namedtuple("UpdateNode", "table Set Where")
DeleteNode = namedtuple("DeleteNode", "From Where")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        # Remove comments
        self.tokens = list(filter(lambda t: t.type != "comment", self.tokens))

        trees = []

        while len(self.tokens) > 0:
            trees.append(self.__parse_block())

        return trees

    def __parse_block(self):
        if self.__peek("select"):
            return self.__parse_select()
        elif self.__peek("delete"):
            return self.__parse_delete()
        elif self.__peek("update"):
            return self.__parse_update()
        else:
            raise RuntimeError("Invalid SQL detected \"" + self.tokens[0].value + "\"")

    def __consume(self, expected_type):
        # FIXME give better error message when no token is at position '0'
        token = self.tokens.pop(0)

        if token.type == expected_type:
            return token
        else:
            raise RuntimeError("Expected token type \"" + expected_type +
                    "\", but got \"" + token.type + "\"")

    def __peek(self, expected_type, offset=0):
        if len(self.tokens) > 0:
            return self.tokens[offset].type == expected_type
        else:
            return False

    def __parse_string(self):
        string = self.__consume("string").value

        if string.startswith("'") and string.endswith("'"):
            string = string[1:-1]

        return StringNode(value=string)

    def __parse_integer(self):
        return IntegerNode(value=int(self.__consume("integer").value))

    def __parse_boolean(self):
        value = None

        if self.__peek("true"):
            self.__consume("true")
            value = True
        elif self.__peek("false"):
            self.__consume("false")
            value = False
        else:
            raise TypeError("\"" + self.tokens[0].value + "\" is not of type boolean")

        return BooleanNode(value=value)

    def __parse_null(self):
        self.__consume("null")
        return NullNode(value=None)

    def __parse_name(self):
        name = self.__consume("name").value

        if name.startswith("[") and name.endswith("]"):
            name = name[1:-1]

        return NameNode(value=name)

    def __parse_from(self):
        self.__consume("from")
        table = self.__parse_name()
        return FromNode(table=table)

    def __parse_where(self):
        self.__consume("where")

        # IN, NOT IN, SQL statement
        # IN
        # NOT IN
        # ( ... ) - Could contain a SELECT, or a set of values (comma-separated)
        if self.__peek("IN"):
            pass

        # AND
        # OR
        # NOT
        # NULL
        # =
        # *
        # /
        # -
        # <> !=
        # <
        # >
        # <=
        # >=
        # integer
        # boolean
        # string
        # other values in the table (e.g. table-name.column)

        #return WhereNode(expression=None)

    def __parse_set(self):

        col = self.__parse_name()

        self.__consume("equal")

        if self.__peek("integer"):
            new = self.__parse_integer()
        elif self.__peek("string"):
            new = self.__parse_string()
        elif self.__peek("true") or self.__peek("false"):
            new = self.__parse_boolean()
        elif self.__peek("null"):
            new = self.__parse_null()
        else:
            raise TypeError("\"" + self.tokens[0].value + "\" is not a valid type")

        return SetNode(column=col, value=new)


    def __parse_select(self):
        self.__consume("select")

        # Handle 'SELECT *'
        if self.__peek("asterisk"):
            self.__consume("asterisk")
            columns=None # NOTE: a 'None' value means "select all columns"

        # Manually specifiing columns
        elif self.__peek("name"):
            columns = []

            columns.append(self.__parse_name())

            while (self.__peek("comma")):
                self.__consume("comma")
                columns.append(self.__parse_name())

        else:
            raise RuntimeError("\"SELECT\" must be followed by a column name")

        from_node = self.__parse_from()

        where_node = None

        if self.__peek("where"):
            where_node = self.__parse_where()

        return SelectNode(columns=columns, From=from_node, Where=where_node)

    def __parse_delete(self):
        self.__consume("delete")

        from_node = self.__parse_from()

        where_node = None

        if self.__peek("where"):
            where_node = self.__parse_where()

        return DeleteNode(From=from_node, Where=where_node)

    def __parse_update(self):
        self.__consume("update")

        table = self.__parse_name()

        self.__consume("set")

        sets = []

        sets.append(self.__parse_set())

        while self.__peek("comma"):
            self.__consume("comma")
            sets.append(self.__parse_set())

        where = None

        if self.__peek("where"):
            where_node = self.__parse_where()

        return UpdateNode(table=table, Set=sets, Where=where)
