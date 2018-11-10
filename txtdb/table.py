import re
from helpers import table_to_file_name

# TODO Datetime data type
# TODO Foreign keys

class Table:
    def __init__(self, table_name, database_dir):
        self.name = table_name
        self.rows = []
        self.__build_table(table_name, database_dir)
        print(self.types)

    def __build_table(self, table_name, database_dir):
        fh = open(table_to_file_name(database_dir, table_name), "r")

        self.__parse_data_types(fh.readline())
        self.col_names = self.__parse_column_names(fh.readline())

        for row in fh:
            self.insert_row(self.__parse_row(row))

        fh.close()

    def __parse_data_types(self, type_string):
        types = type_string.strip().split(",")
        self.types = []

        for idx, val in enumerate(types):
            if val.startswith("string"):
                col_type = str
            elif val.startswith("int"):
                col_type = int
            elif val.startswith("boolean"):
                col_type = bool
            else:
                col_type = None

            self.types.append({
                "type": col_type,
                "nullable": True if val[-1:] == "?" else False,
                "primary key": True if val[-1:] == "$" else False
            })

    def __parse_column_names(self, input_string):
        return list(map(lambda c: c.replace("\"", ""), input_string.split(",")))

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

    def insert_row(self, row):
        for idx, field in enumerate(row):
            print(field)
            if (type(field) == self.types[idx]["type"]):
                self.rows.append(row)
            elif (field == None and self.types[idx]["nullable"] == True):
                self.rows.append(row)
            else:
                raise TypeError("Value \"" + str(field) + "\" is not of type \"" + str(self.types[idx]["type"]) + "\"")

    # def write_table(self):
    #     # fh = open(table_to_file_name(self.name), "w")
    #     pass

    # def __fields_to_str(self, field):
    #     if (isinstance(field, str)):
    #         return "\"" + field.replace(",", "\\,") + "\""
    #     else:
    #         return str(field)
