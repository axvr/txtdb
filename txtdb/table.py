from helpers import table_to_file_name

class Table:
    def __init__(self, table_name, database_dir):
        self.__build_table(table_name, database_dir)

    def __build_table(self, table_name, database_dir):
        # TODO error handling
        fh = open(table_to_file_name(database_dir, table_name), "r")
        for line in fh:
            print(line) # TODO parse file
        fh.close()
