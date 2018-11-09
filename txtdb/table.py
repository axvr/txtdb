import re
from helpers import table_to_file_name

class Table:
    def __init__(self, table_name, database_dir):
        self.__build_table(table_name, database_dir)

    def __build_table(self, table_name, database_dir):
        # TODO error handling
        fh = open(table_to_file_name(database_dir, table_name), "r")

        # Data type
        col_types = self.__parse_data_types(fh.readline())

        # Column name
        col_names = self.__parse_column_names(fh.readline())

        # Rows
        for line in fh:
            self.__parse_row(line)

        fh.close()

    # TODO handle column attributes
    def __parse_data_types(self, input_string):
        return input_string.split(",")

    def __parse_column_names(self, input_string):
        return map(lambda c: c.replace("\"", ""), input_string.split(","))

    # TODO escape commas in strings
    # TODO enclose strings in quotes
    def __parse_row(self, input_string):
        print(re.split('(?:(?<!\\\),)', input_string.strip()))

    def insert_row(self):
        return

    def validate_table(self):
        return
