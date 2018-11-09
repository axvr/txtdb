from helpers import file_to_table_name, get_table_list
from table import Table

class Database():
    def __init__(self, database_dir):
        self.database_dir = database_dir
        self.refresh()

    def refresh(self):
        self.tables = { }
        for table in get_table_list(self.database_dir):
            self.tables[table] = Table(table, self.database_dir)
