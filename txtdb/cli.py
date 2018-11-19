from optparse import OptionParser

def parse_cli_options():
    parser = OptionParser()
    parser.add_option("-d", "--database", dest="database", default="example",
            help="Specifiy the path to the database directory")
    return parser.parse_args()
