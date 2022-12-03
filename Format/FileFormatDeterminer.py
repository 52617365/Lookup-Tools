from dataclasses import dataclass

from Format.Input import get_file_fields_from_user, get_file_delimiter_from_user


@dataclass
class FileFormat:
    fields: list
    ignored_fields: list
    file_delimiter: str


class FileFormatDeterminer:
    @staticmethod
    def determine_file_format(database_path: str) -> FileFormat:
        FileFormatDeterminer.express_file_format(database_path)
        file_fields = get_file_fields_from_user()
        file_delimiter = get_file_delimiter_from_user()
        ignored_fields = FileFormatDeterminer.get_ignored_fields(file_fields)
        return FileFormat(fields=file_fields, ignored_fields=ignored_fields, file_delimiter=file_delimiter)

    @staticmethod
    def express_file_format(database_path: str):
        n_lines = FileFormatDeterminer.read_the_first_n_lines_from_file_whilst_deleting_new_lines(database_path)
        FileFormatDeterminer.print_lines_to_user(n_lines, database_path)

    @staticmethod
    def read_the_first_n_lines_from_file_whilst_deleting_new_lines(database_path: str) -> list:
        try:
            lines_to_read = 5
            with open(database_path, 'r') as file:
                n_lines = [FileFormatDeterminer.delete_line_breaks(next(file)) for _ in range(lines_to_read)]
                return n_lines
        except IOError:
            quit(F"File {database_path} does not exist or it's not accessible.")

    @staticmethod
    def delete_line_breaks(line):
        return line.rstrip()

    @staticmethod
    def print_lines_to_user(lines: list, database_path: str):
        print(F"Database path: {database_path}")
        print(F"Printing the first {len(lines)} lines.")
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
