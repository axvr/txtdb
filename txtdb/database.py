"""Create a new database instance"""

from os import listdir, remove
from os.path import isfile, join
from helpers import file_to_table_name, table_to_file_name
from table import Table

class Database(object):
    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.tables = {}
        self.reload()

    def reload(self):
        """Reload the database tables from the table files"""
        for table in self.__get_table_files():
            self.tables[table] = Table(table, self.database_dir)

    def create_table(self, name, columns):
        """Create a new table in the database"""
        if name not in self.tables:
            # TODO ensure columns are in valid format
            self.tables[name] = Table(name, self.database_dir, columns)
        else:
            raise NameError("Table with name \"" + name + "\" already exists")

    def write(self):
        """Save all changes to the database"""
        for table in self.tables:
            self.tables[file_to_table_name(table)].write()

    def drop(self, table):
        if self.tables.pop(table, None) is None:
            raise NameError("Table with name \"" + table + "\" doesn't exist")

        f = table_to_file_name(self.database_dir, table)
        if isfile(f):
            remove(f)

    def __get_table_files(self):
        for f in listdir(self.database_dir):
            if (isfile(join(self.database_dir, f)) and f.endswith(".csv")):
                yield file_to_table_name(f)
