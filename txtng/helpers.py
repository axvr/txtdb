from os.path import join, basename

def table_to_file_name(database_dir, table_name):
    return join(database_dir, table_name + ".csv")

def file_to_table_name(file_path):
    return basename(file_path).replace(".csv", "")
