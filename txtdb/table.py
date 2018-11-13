import re
from helpers import table_to_file_name

# TODO Foreign keys and table relationships
# TODO provide mechanism to create new tables
# TODO update and delete

class Table:
    def __init__(self, table_name, database_dir):
        self.name = table_name
        self.dir = database_dir
        self.rows = []
        self.__build_table()

    def __build_table(self):
        fh = open(table_to_file_name(self.dir, self.name), "r")

        self.columns = self.__parse_header(fh.readline(), fh.readline())

        for row in fh:
            self.insert(self.__parse_row(row))

        fh.close()

    def __parse_header(self, types, names):
        columns = []
        names_list = list(map(lambda c: c.replace("\"", ""), names.strip().split(",")))

        for idx, val in enumerate(types.strip().split(",")):
            if val.startswith("string"):
                col_type = str
            elif val.startswith("int"):
                col_type = int
            elif val.startswith("boolean"):
                col_type = bool
            else:
                col_type = None

            columns.append({
                "name": names_list[idx],
                "type": col_type,
                "nullable": True if val[-1:] == "?" else False,
                "primary key": True if val[-1:] == "$" else False
            })

        return columns

    def __parse_row(self, row):
        return list(map(self.__cast_fields, re.split("(?:(?<!\\\),)", row.strip())))

    def __cast_fields(self, field):
        if (field.lower() == "true"):
            return True
        elif (field.lower() == "false"):
            return False
        elif (re.match("^\d+$", field)):
            return int(field)
        elif (re.match("^\".*\"$", field)):
            return field[1:-1].replace("\\,", ",")
        else:
            return None

    def __get_column_index(column):
        for i, v in enumerate(col_names):
            if (v == column):
                return i

    def insert(self, row):
        for idx, field in enumerate(row):
            if ((self.columns[idx]["primary key"] == True) and (any(field in sub[idx] for sub in self.rows))):
                raise KeyError("Primary key \"" + field + "\" already exists")
            elif (type(field) == self.columns[idx]["type"]):
                continue
            elif (field == None and self.columns[idx]["nullable"] == True):
                continue
            else:
                raise TypeError("Value \"" + str(field) + "\" is not of type \"" + str(self.columns[idx]["type"]) + "\"")
        self.rows.append(row)

    def write(self):
        fh = open(table_to_file_name(self.dir, self.name), "w+")

        contents = []

        (names, types) = self.__construct_file_header()

        contents.append(types)
        contents.append(names)

        for row in self.rows:
            contents.append(self.__construct_data_row(row))

        fh.writelines(contents)
        fh.close

    def __construct_data_row(self, original_row):
        row = ""

        for field in original_row:
            if (isinstance(field, str)):
                row = row + "\"" + field.replace(",", "\\,") + "\"" + ","
            elif (isinstance(field, bool)):
                row = row + str(field).lower() + ","
            elif (field == None):
                row = row + ","
            else:
                row = row + str(field) + ","

        return row[:-1] + "\n"

    def __construct_file_header(self):
        types = ""
        names = ""

        for col in self.columns:
            names = names + "\"" + col["name"] + "\","

            # Types
            if (col["type"] == str):
                col_type = "string"
            elif (col["type"] == int):
                col_type = "int"
            elif (col["type"] == bool):
                col_type = "boolean"
            else:
                col_type = ""

            # Attributes
            attrs = ""
            if (col["nullable"] == True):
                attrs = attrs + "?"
            elif (col["primary key"] == True):
                attrs = attrs + "$"

            types = types + col_type + attrs + ","

        # Remove trailing commas
        names = names[:-1] + "\n"
        types = types[:-1] + "\n"

        return (names, types)
