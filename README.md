# txtdb

An attempt to create a simple database engine and RDBMS which stores the table
data in text files, using the CSV format.

**Please do not use this for anything important**, it was created as a learning
project.


## Table specification

Example of a table stored by _txtdb_:

```csv
string$,string,boolean?,int?
"id","name","pass","score"
"d928ffe1-cef4-41fd-8123-f2ef7b009a69","John Smith",true,91
"6f2b874a-7849-4115-a6c8-9bae8918f886","Jane Doe",false,62
"49064480-4056-4a08-aff9-4af9580f1879","Bob",,
"48da7211-3648-4a8e-85d1-8d68c6161653","Alice",true,95
```

The table files are stored in the CSV format, for easy parsing by other tools.

The first line of a file specifies the data type of each column and sets the
attributes for each of the columns.

The second line just holds a list of each of the names of the columns.


### Table names

The table name is simply the file name without the extension.


### Data types

- `string`   (e.g. `"something"`)
- `int`      (e.g. `12345`)
- `boolean`  (e.g. `true`)
<!-- - `datetime` (e.g. `2018-11-09`) -->

(Note: when strings are stored, any commas will be escaped in the table CSV file).


### Column attributes

Columns can be given different "attributes", which can change their behaviour.
Column attributes are appended to the end of the datatype (e.g. `,string?,`).

The currently available attributes are:

- `$`: Primary key
<!-- - `%`: Foreign key -->
- `?`: Nullable column

At the moment there is a maximum of one attribute per column.


### Null values

If a column has the `?` (null) attribute, then null values can be stored in
that column. A null value is represented by an empty CSV field.


[//]: https://en.wikipedia.org/wiki/Relational_database (Releational database)
[//]: https://en.wikipedia.org/wiki/Unique_key (Prmiary key)
[//]: https://en.wikipedia.org/wiki/Foreign_key (Foreign key)
[//]: https://en.wikipedia.org/wiki/Comma-separated_values (Comma-separated values)
