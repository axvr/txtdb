# Read data from the tables

from helpers import file_to_table_name, table_to_file_name, get_table_list

TEST_TABLE = "database/example.csv"

class Reader():
    def __init__(self, database_dir):
        self.database_dir = database_dir

    def open_table(table_name):
        filehandle = open(TEST_TABLE, "r")
        for line in filehandle:
            print(line)
