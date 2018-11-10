from helpers import file_to_table_name
from table import Table
from os import listdir
from os.path import isfile, join

class Database():
    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.refresh()

    def refresh(self):
        self.tables = { }
        for table in self.get_table_list():
            self.tables[table] = Table(table, self.database_dir)

    def get_table_list(self):
        for f in listdir(self.database_dir):
            if (isfile(join(self.database_dir, f))):
                yield file_to_table_name(f)

# db.tables['example'].row()
