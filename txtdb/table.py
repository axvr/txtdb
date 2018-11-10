import re
from helpers import table_to_file_name

class Table:
    def __init__(self, table_name, database_dir):
        self.rows = []
        self.__build_table(table_name, database_dir)
        print(self.rows)

    def __build_table(self, table_name, database_dir):
        # TODO error handling
        fh = open(table_to_file_name(database_dir, table_name), "r")

        # Data type
        self.col_types = self.__parse_data_types(fh.readline())

        # Column name
        self.col_names = self.__parse_column_names(fh.readline())

        # Rows
        for line in fh:
            self.insert_row(self.__parse_row(line))

        fh.close()

    # TODO handle column attributes (mainly nullable values)
    def __parse_data_types(self, input_string):
        return input_string.split(",")

    def __parse_column_names(self, input_string):
        return map(lambda c: c.replace("\"", ""), input_string.split(","))

    def __parse_row(self, row):
        return list(map(self.__cast_fields, re.split("(?:(?<!\\\),)", row.strip())))

    def __cast_fields(self, field):
        if (field == "true"):
            return True
        elif (field == "false"):
            return False
        elif (re.match("^\d+$", field)):
            return int(field)
        elif (re.match("^\".*\"$", field)):
            return field[1:-1].replace("\\,", ",")
        elif (True == False):
            # TODO Datetime
            pass
        else:
            return None

    def __get_column_index(column):
        for i, v in enumerate(col_names):
            if (v == column):
                return i

    # TODO validate row data before appending
    def insert_row(self, row):
        for index, field in enumerate(row):
            print(type(field))
        self.rows.append(row)

    # TODO escape commas in strings
    # TODO enclose strings in quotes
    def write_table(self):
        pass
