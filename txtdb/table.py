"""Create a new table instance"""

import re
from helpers import table_to_file_name

# TODO Foreign keys and table relationships

class Table(object):
    def __init__(self, table_name, database_dir, columns=None):
        self.name = table_name
        self.dir = database_dir
        self.rows = []

        if columns is None:
            self.__parse_table_file(table_to_file_name(self.dir, self.name))
        else:
            self.columns = columns

    def __parse_table_file(self, table_file):
        fh = open(table_file, "r")

        self.columns = self.__parse_header(fh.readline(), fh.readline())

        for row in fh:
            self.insert(self.__parse_row(row))

        fh.close()

    def __parse_header(self, types, names):
        columns = []
        names_list = list(map(lambda c: c.replace("\"", ""), names.strip().split(",")))

        for idx, val in enumerate(types.strip().split(",")):
            if val.startswith("string"):
                col_type = str
            elif val.startswith("int"):
                col_type = int
            elif val.startswith("boolean"):
                col_type = bool
            else:
                col_type = None

            columns.append({
                "name": names_list[idx],
                "type": col_type,
                "nullable": True if val[-1:] == "?" else False,
                "primary key": True if val[-1:] == "$" else False
            })

        return columns

    def __parse_row(self, row):
        return list(map(self.__cast_field, re.split(r"(?<!\\),", row.strip())))

    def __cast_field(self, field):
        if field.lower() == "true":
            return True
        elif field.lower() == "false":
            return False
        elif re.match("^\d+$", field):
            return int(field)
        elif re.match("^\".*\"$", field):
            return field[1:-1].replace("\\,", ",")
        else:
            return None

    def __get_column_index(column):
        for i, v in enumerate(col_names):
            if v == column:
                return i

    def __check_row_is_valid(self, row, check_pk=True):
        for idx, field in enumerate(row):
            if (check_pk and (self.columns[idx]["primary key"] is True) and (any(field in sub[idx] for sub in self.rows))):
                raise KeyError("Primary key \"" + field + "\" already exists")
            elif (type(field) == self.columns[idx]["type"]):
                continue
            elif (field is None and self.columns[idx]["nullable"] is True):
                continue
            else:
                raise TypeError("Value \"" + str(field) + "\" is not of type \"" + str(self.columns[idx]["type"]) + "\"")
        return True

    def insert(self, row):
        """Insert a new row into the table"""
        if self.__check_row_is_valid(row):
            self.rows.append(row)

    def write(self):
        """Save changes to the table"""
        fh = open(table_to_file_name(self.dir, self.name), "w+")

        contents = []

        (names, types) = self.__construct_file_header()

        contents.append(types)
        contents.append(names)

        for row in self.rows:
            contents.append(self.__construct_data_row(row))

        fh.writelines(contents)
        fh.close

    def delete(self, row):
        """Delete a row from the table"""
        try:
            self.rows.remove(row)
        except ValueError:
            raise ValueError("Row \"" + str(row) + "\" does not exist")

    def update(self, original, updated):
        """Change a row in the table"""
        if self.__check_row_is_valid(updated, check_pk=False):
            for idx, row in enumerate(self.rows):
                if row == original:
                    self.rows[idx] = updated
                    return
            raise ValueError("Row \"" + str(row) + "\" does not exist")

    def select(self):
        """Return all rows in the table, and the column information"""
        return (self.columns, self.rows)

    def __construct_data_row(self, original_row):
        row = ""

        for field in original_row:
            if (isinstance(field, str)):
                row = row + "\"" + field.replace(",", "\\,") + "\"" + ","
            elif (isinstance(field, bool)):
                row = row + str(field).lower() + ","
            elif (field is None):
                row = row + ","
            else:
                row = row + str(field) + ","

        return row[:-1] + "\n"

    def __construct_file_header(self):
        types = ""
        names = ""

        for col in self.columns:
            names = names + "\"" + col["name"] + "\","

            # Types
            if (col["type"] == str):
                col_type = "string"
            elif (col["type"] == int):
                col_type = "int"
            elif (col["type"] == bool):
                col_type = "boolean"
            else:
                col_type = ""

            # Attributes
            attrs = ""
            if (col["nullable"] is True):
                attrs = attrs + "?"
            elif (col["primary key"] is True):
                attrs = attrs + "$"

            types = types + col_type + attrs + ","

        # Remove trailing commas
        names = names[:-1] + "\n"
        types = types[:-1] + "\n"

        return (names, types)
