from os import listdir
from os.path import isfile, join, basename

def table_to_file_name(database_dir, table_name):
    return join(database_dir, table_name + ".csv")

def file_to_table_name(file_name):
    return basename(file_name).replace(".csv", "")

def get_table_list(database_dir):
    for f in listdir(database_dir):
        if (isfile(join(database_dir, f))):
            yield file_to_table_name(f)
