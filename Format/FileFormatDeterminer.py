from dataclasses import dataclass

from Format.Input import print_file_format_instructions, print_file_delimiter_instructions, get_file_fields_from_user, \
    get_file_delimiter_from_user


@dataclass
class FileFormat:
    fields: list
    ignored_fields: list
    file_delimiter: str


class FileFormatDeterminer:
    def __init__(self, database_path: str, n: int = 5):
        self.database_path = database_path
        self.n = n

    def determine_file_format(self) -> FileFormat:
        self.express_file_format()
        file_fields = get_file_fields_from_user()
        file_delimiter = get_file_delimiter_from_user()
        ignored_fields = self.get_ignored_fields(file_fields)
        return FileFormat(fields=file_fields, ignored_fields=ignored_fields, file_delimiter=file_delimiter)

    def express_file_format(self):
        print_file_format_instructions()
        print_file_delimiter_instructions()
        n_lines = self.read_the_first_n_lines_from_file_whilst_deleting_new_lines()
        self.print_lines_to_user(n_lines)

    def read_the_first_n_lines_from_file_whilst_deleting_new_lines(self) -> list:
        try:
            with open(self.database_path, 'r') as file:
                n_lines = [self.delete_line_breaks(next(file)) for _ in range(self.n)]
                return n_lines
        except IOError:
            quit(F"File {self.database_path} does not exist or it's not accessible.")

    @staticmethod
    def delete_line_breaks(line):
        return line.rstrip()

    def print_lines_to_user(self, lines: list):
        print(F"Database path: {self.database_path}")
        print(F"Printing the first {self.n} lines.")
        print("Please specify the format of the file.")
        for line in lines:
            print(line)
        print("\n\n")

    @staticmethod
    def get_ignored_fields(user_input: list) -> list:
        ignored_fields = []
        for field in user_input:
            if field_is_ignored(field):
                ignored_fields.append(field)
        return ignored_fields


def field_is_ignored(field: str) -> bool:
    return field.startswith("_")
