
def print_welcome_message():
    print("This program is a Push-Down Automata (PDA) string simulator.")
    print("Given a PDA provided as a JSON file under files/, it will generate its transition table.")
    print("With this transition table, it will then loop through the provided strings and print whether it is accepted or rejected.")


def print_menu():
    print("Actions:")
    print("1. Loop through strings in JSON file")
    print("2. Enter in string manually")
    print("3. Print PDA transition table")
    print("4. Move to next file in files/ directory.")
    print("5. Exit program")

def print_transition_table_info(filename):
    print(f"Transition table for {filename}")
    print("Each cell in the table is comprised of a state to transtion on the character in the column as well as the action to perform on the stack.")
    print("Ex: q1 (E/E) under column 'a', would mean to transition to state q1 on a and replace lambda with labmda.")
    print("* Note: Formatting may be off on non-deterministic PDAs with many transitions on one character.")


def get_user_input():
    """
    Get the user's input to perform an action
    """

    ret = input("Enter action: ")

    while not ret:
        ret = input("Enter action: ")

    return ret

def get_user_string():
    """
    Gets the user's desired string
    """
    ret = input("Enter in a string to test (for the empty string only press ENTER): ")

    return ret

