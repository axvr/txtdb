from optparse import OptionParser

def main():
    parse_cli_options()
    print("Hello world!") # TODO Begin main program execution

def parse_cli_options():
    """https://docs.python.org/3.1/library/optparse.html#module-optparse"""
    parser = OptionParser()
    parser.parse_args()
