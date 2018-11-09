from helpers import file_to_table_name, table_to_file_name, get_table_list

class Database():
    def __init__(self, database_dir):
        self.database_dir = database_dir

    def reload(self):
        for table in get_table_list(self.database_dir):
            self.parse_table_file(table)

    def parse_table_file(self, table_name):
        # TODO error handling
        filehandle = open(table_to_file_name(self.database_dir, table_name), "r")
        for line in filehandle:
            print(line) # TODO parse file
        filehandle.close()
