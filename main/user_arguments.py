import argparse


class CommandLineArguments:

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='A program that parses delimited files')
        self.parser.add_argument('-s', '--search', default='cat', type=str, help='search term')
        self.parser.add_argument('-n', '--num_images', default=5, type=int, help='num images to save')
        self.parser.add_argument('-d', '--directory', default='downloads', type=str, help='save directory')
        self.args = self.parser.parse_args()

    def get_arguments(self):
        return self.args
