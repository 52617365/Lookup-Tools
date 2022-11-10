import os


def is_valid_file(file_path):
    return os.path.isfile(file_path)


def get_file_without_path_or_extension(file_name):
    return os.path.splitext(os.path.basename(file_name))[0]
