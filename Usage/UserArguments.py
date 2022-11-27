import argparse


class CommandLineArguments:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Parse delimited files into JSON strings')
        self.parser.add_argument('-i', '--input', type=str, help='The delimited file that should be parsed to JSON',
                                 required=True)
        self.parser.add_argument('-a', '--additional', type=str,
                                 help='The path to the additional database information', required=True)
        self.parser.add_argument('-g', '--glob', default=False, type=bool,
                                 help='A boolean value to determine if the input is a glob', required=False)
        self.parser.add_argument('-j', '--json', default=False, type=bool,
                                 help='A boolean flag to determine if the file user is trying to import is JSON:',
                                 required=False)
        self.args = self.parser.parse_args()

    def get(self):
        return self.args
