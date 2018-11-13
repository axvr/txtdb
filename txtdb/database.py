from helpers import file_to_table_name
from table import Table
from os import listdir
from os.path import isfile, join

class Database():
    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.reload()

    def reload(self):
        """Reload the database tables based on the table files"""
        self.tables = { }
        for table in self.__get_table_files():
            self.tables[table] = Table(table, self.database_dir)

    def write(self):
        """Save all database changes"""
        for table in self.tables:
            self.tables[file_to_table_name(table)].write()

    def __get_table_files(self):
        for f in listdir(self.database_dir):
            if (isfile(join(self.database_dir, f))):
                yield file_to_table_name(f)
