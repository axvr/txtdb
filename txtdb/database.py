"""Create a new database instance"""

from os import listdir, remove
from os.path import isfile, join
from distutils.dir_util import mkpath
from distutils.file_util import copy_file
from datetime import datetime

from helpers import file_to_table_name, table_to_file_name
from table import Table

# TODO backups and transactions

class Database():

    def __init__(self, database_dir, ignore_lock=False):
        """Constructor: create new db instance"""
        self.database_dir = database_dir

        # Database locking
        self.locked = False
        self.lock_file = join(database_dir, 'db.lock')

        if isfile(self.lock_file) and not ignore_lock:
            raise RuntimeError('The database is in use/locked')
        elif not isfile(self.lock_file):
            open(self.lock_file, 'a').close()
            self.locked = True

        # Load the data from disk
        self.tables = {}
        self.reload()

    def __del__(self):
        """Destructor: destroy the db instance"""
        # Remove the lock file (but, only if this instance created it)
        if isfile(self.lock_file) and self.locked:
            remove(self.lock_file)

    def __get_table_files(self):
        for f in listdir(self.database_dir):
            if isfile(join(self.database_dir, f)) and f.endswith(".csv"):
                yield file_to_table_name(f)

    def reload(self):
        """Reload the database tables from the table files"""
        for table in self.__get_table_files():
            self.tables[table] = Table(table, self.database_dir)

    def write(self):
        """Write all changes to the database"""
        for table in self.tables:
            table.write()

    def create_table(self, name, columns):
        """Create a new table in the database"""
        if name in self.tables:
            raise NameError("Table \"" + name + "\" already exists")

        # TODO check that columns is valid
        self.tables[name] = Table(name, self.database_dir, columns)

    def drop_table(self, table):
        """Remove table from the database"""
        if self.tables.pop(table, None) is None:
            raise NameError("Table \"" + table + "\" doesn't exist")

        # FIXME: This causes a change to the saved database, which wouldn't
        # work with the planned transaction feature
        f = table_to_file_name(self.database_dir, table)
        if isfile(f):
            remove(f)


    def create_backup(self, name="backup"):
        """Create a full backup of the database table files"""
        backup_dir = join(self.database_dir,
                name + str(datetime.utcnow().strftime("_%Y-%m-%d_%H:%M:%S")))
        mkpath(backup_dir)
        for table in self.__get_table_files():
            copy_file(table_to_file_name(self.database_dir, table), backup_dir)

    def restore_backup(self, version=None):
        """Restore from one of the database backups"""
        # TODO if version not specified, restore latest
        pass

    def create_transaction(self):
        pass

    def commit_transaction(self):
        pass

    def rollback_transaction(self):
        pass
