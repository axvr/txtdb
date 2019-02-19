# txtql - txtdb Query Language

This is the code for the txtdb SQL compiler. Just like with txtdb itself, this
is an experiment and a learning project. It is not designed to be efficient in
in the slightest, and will likely never gain any optimisations (which would be
difficult anyway since it is written in Python).

## Structure

### Tokeniser

This module splits up the SQL query into individual tokens using a hierarchical
list of _regular expressions_. It makes the job of the parser much simpler, and
allows for the easy removal of parts of the query, such as comments.

### Parser

The parser takes the list of tokens and converts it into an "_abstract syntax
tree_" -- an internal representation of the entered query -- through _lexical
analysis_.

### Generator

The generator performs the job of converting the "abstract syntax tree" into
working Python code, which interacts with the database-engine to perform the
action(s) specified by the original SQL query.

## Attribution

This compiler is based on the one created in [this excellent
screencast](https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch)
by Gary Bernhardt of [Destroy All Software](https://www.destroyallsoftware.com/).
