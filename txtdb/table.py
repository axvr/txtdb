import re
from helpers import table_to_file_name

# TODO Foreign keys
# TODO store column names in the same object as the column types

class Table:
    def __init__(self, table_name, database_dir):
        self.name = table_name
        self.rows = []
        self.__build_table(table_name, database_dir)

    def __build_table(self, table_name, database_dir):
        fh = open(table_to_file_name(database_dir, table_name), "r")

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
            if (type(field) == self.columns[idx]["type"]):
                self.rows.append(row)
            elif (field == None and self.columns[idx]["nullable"] == True):
                self.rows.append(row)
            else:
                raise TypeError("Value \"" + str(field) + "\" is not of type \"" + str(self.columns[idx]["type"]) + "\"")

    # def write(self):
    #     # fh = open(table_to_file_name(self.name), "w")
    #     pass

    # def __fields_to_str(self, field):
    #     if (isinstance(field, str)):
    #         return "\"" + field.replace(",", "\\,") + "\""
    #     else:
    #         return str(field)
