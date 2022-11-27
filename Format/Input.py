def get_file_format_from_user():
    user_input = input("Enter the format of the file:\t").strip()

    if user_input == "idk":
        print("Okay, skipping this one.")
        # TODO: return or something.

    validate_format_user_input(user_input)

    file_format = user_input.split(",")

    return file_format


def validate_format_user_input(user_input):
    if len(user_input) == 0:
        print("You didn't specify a format. If you don't know, input 'idk'.", flush=True)
        get_file_format_from_user()


def get_file_delimiter_from_user():
    file_delimiter = input("Enter the delimiter of the file:\t").strip()

    if file_delimiter == "idk":
        print("Okay, skipping this one.")
        # TODO: return or something.

    validate_delimiter(file_delimiter)

    return file_delimiter


def validate_delimiter(user_input):
    if len(user_input) == 0:
        print("You didn't specify a delimiter. If you don't know, input 'idk'.", flush=True)
        get_file_delimiter_from_user()
    if len(user_input) > 1:
        print("You specified a delimiter that is more than one character. Please specify a single character.",
              flush=True)
        get_file_delimiter_from_user()


def print_file_format_instructions():
    print("=======Format Instructions=======")
    print("Determine the file format with the following options:")
    print("- 'idk' if you don't know the format.")
    print("- prefix fields with '_' if you want to ignore them.")
    print("- specify the format as a comma delimited sequence of characters.")
    print("example format input:\t_id,name,age\n")


def print_file_delimiter_instructions():
    print("=======Delimiter Instructions=======")
    print("Determine the file delimiter with the following options:")
    print("- 'idk' if you don't know the delimiter.")
    print("- specify the delimiter as a single character.")
    print("example delimiter input:\t,\n")
