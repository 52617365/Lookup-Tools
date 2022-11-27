from dataclasses import dataclass

from Format.Input import print_file_format_instructions, print_file_delimiter_instructions, get_file_format_from_user, \
    get_file_delimiter_from_user


@dataclass
class FileFormat:
    format: list
    delimiter: str


class FileFormatDeterminer:
    def __init__(self, database_path: str, n: int):
        self.database_path = database_path
        self.n = n

    # TODO: caller of this should catch IDKException and StopIteration and skip when caught.
    def determine(self) -> FileFormat | None:
        self.express_file_format()
        file_format = get_file_format_from_user()
        file_delimiter = get_file_delimiter_from_user()
        return FileFormat(file_format, file_delimiter)

    def express_file_format(self):
        print_file_format_instructions()
        print_file_delimiter_instructions()
        n_lines = self.read_the_first_n_lines_from_file_whilst_deleting_new_lines()
        self.print_lines_to_user(n_lines)

    def read_the_first_n_lines_from_file_whilst_deleting_new_lines(self) -> list:
        try:
            with open(self.database_path, 'r') as file:
                n_lines = [next(file).rstrip() for _ in range(self.n)]
                return n_lines
        except IOError:
            quit(F"File {self.database_path} does not exist or it's not accessible.")

    def print_lines_to_user(self, lines: list):
        print(F"printing the first {self.n} lines of {self.database_path}, please specify the format of the file.\n")
        for line in lines:
            print(line)
        print("\n\n")

# TODO: this should not be called from here, instead call it when we're reading the csv.
# @staticmethod
# def get_ignored_fields(user_input: list) -> list:
#     ignored_fields = []
#     for field in user_input:
#         if field.startswith("_"):
#             ignored_fields.append(field)
#     return ignored_fields