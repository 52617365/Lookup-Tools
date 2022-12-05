import argparse


class CommandLineArguments:

    def __init__(self):
        self.parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description=
        '=======Format Instructions=======\n'
        'Determine the file format with the following options:\n'
        '* "idk" if you dont know the format.\n'
        '* prefix fields with "_" if you want to ignore them.\n'
        '* specify the format as a comma delimited sequence of characters.\n'
        'example format input: "_id,name,age"\n\n'
        '=======Delimiter Instructions=======\n'
        'Determine the file delimiter with the following options:\n'
        '* "idk" if you dont know the delimiter.\n'
        '* specify the delimiter as a single character.\n'
        'example delimiter input: ","\n')
        self.parser.add_argument('-i', '--input', type=str, help='The delimited file that should be parsed to JSON',
                                 required=True)
        self.parser.add_argument('-a', '--additional', type=str,
                                 help='The path to the additional database information', required=True)
        self.parser.add_argument('-g', '--glob', default=False, type=bool,
                                 help='A boolean value to determine if the input is a glob', required=False)
        self.parser.add_argument('-m', '--manual', default=True, type=bool,
                                 help='A boolean value to determine if the format should be specified by the user. If this flag is false, the format has to be on the first line of the file.',
                                 required=False)
        self.parser.add_argument('-s', '--skip_invalid_lines', default=False, type=bool,
                                 help='A boolean value to determine if the program should skip invalid lines. Default is false.',
                                 required=False)
        self.args = self.parser.parse_args()
        # TODO its not parsing -m correctly when passed in with the -m false flag.

    def get(self):
        return self.args
