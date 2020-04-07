import json
from os.path import splitext


def read_file(file_name):
    # Check to see if the file is JSON
    f_name, ext = splitext(file_name)


    if ext.lower() != ".json":
        print(f"File \"{file_name}\" is not a .json file.")
        return False

    try:
        with open(file_name) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Could not find file: '{file_name}'")

    return data
