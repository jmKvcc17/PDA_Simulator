import os, sys
from signal import signal, SIGINT
from resources import json_reader, pda, menu


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting...')
    exit(0)


def main_loop():
    file_dir = './files/'
    user_input = ""

    for file in os.listdir(file_dir):
        data = json_reader.read_file(file_dir + file)

        if data == False:  # If there was an issue with the file
            continue

        print(f"Using PDA: {file}")
        user_pda = pda.PDA(data)  # Create the PDA

        if user_pda.JSON_ERROR:  # If there was an issue reading the JSON file
            continue

        menu.print_welcome_message()  # Print the welcome message
        menu.print_menu()  # Print the menu options
        user_input = menu.get_user_input()  # Print

        while True:

            print()
            if user_input == '1' and user_pda.included_strings:  # Loop through the provided strings in the file
                user_pda.check_strings()
            elif user_input == '2':  # The user manually enters a string
                user_string = menu.get_user_string()
                user_pda.check_string(user_string)
            elif user_input == '3':  # Print the transition table
                menu.print_transition_table_info(file)
                user_pda.user_print_transition_table()
            elif user_input == '4':  # Skip to the next file
                break
            elif user_input == '5':  # Exit the program
                sys.exit()
            else:
                print("Invalid input.")
        
            print()
            menu.print_menu()
            user_input = menu.get_user_input()


if __name__ == "__main__":
    signal(SIGINT, handler)

    main_loop()

    print("No more files, exiting.")

    # file_dir = './files/'
    # # data = json_reader.read_file(file_dir + 'pda_7_1_3.json')
    # data = json_reader.read_file(file_dir + 'pda_single.json')

    # user_pda = pda.PDA(data)  # Create the PDA
    # user_pda.user_print_transition_table()

    # user_pda.check_strings()

    

        