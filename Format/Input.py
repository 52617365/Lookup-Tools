def get_file_format_from_user():
    user_input = get_user_input("Enter the format of the file:\t")

    validate_format_user_input(user_input)

    file_format = user_input.split(",")

    return file_format


def validate_format_user_input(user_input):
    if len(user_input) == 0:
        quit("You didn't specify a format. If you don't know, input 'idk'.")


def get_file_delimiter_from_user():
    user_input = get_user_input("Enter the delimiter of the file:\t")

    validate_delimiter(user_input)

    return user_input


def validate_delimiter(user_input):
    if len(user_input) == 0:
        quit("You didn't specify a delimiter. If you don't know, input 'idk'.")
    if len(user_input) > 1:
        quit("You specified a delimiter that is more than one character. Please specify a single character.")


def get_user_input(text_to_prompt: str):
    user_input = input(text_to_prompt)

    if is_idk_prompt(user_input):
        # TODO: do something here, E.g. skip this file etc.
        return

    return user_input


def is_idk_prompt(user_input: str):
    if user_input == "idk":
        print("Okay, skipping this one.")
        # TODO: return or something.


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
