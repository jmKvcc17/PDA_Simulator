import json
import traceback
from .node import Node
from .node_collection import NodeCollection

class PDA:
    def __init__(self, data):
        self.input_data = data
        self.strings = []

        # Variables
        # PDA
        self.pda_states = []
        self.pda_transitions = []
        self.alphabet = []
        self.end_state = []
        self.pda_stack = [] # Use append() to push, pop() to remove

        # Bools
        self.is_lambda = False # Used to check if the current transition was a lambda transition, as to not consume a character in the string
        self.included_strings = True  # Bool to check if the included JSON file has strings provided
        self.JSON_ERROR = False

        # NFA and DFA construction
        self.JSON_ERROR = self.parse_data()  # Get data from the JSON file

        if self.JSON_ERROR == False:
            print("Creating PDA...")
            # NFA construction
            self.pda_num_rows = len(self.pda_states) + 1
            self.pda_num_cols = len(self.alphabet) + 1
            self.pda_trans_table = [[0 for x in range(self.pda_num_cols)] for y in range(self.pda_num_rows)]
            self.construct_trans_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols, self.pda_transitions, self.pda_states)

            print()
        else:
            print("Error: Cannot construct PDA. Please check JSON file.")
            print()

    def user_print_transition_table(self):
        self.print_transition_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols)

    def check_strings(self):
        """
        Loop through all strings and check if they are accepted by the PDA
        """
        if len(self.strings) == 0:
            print("No strings to test.")
            return False

        for string in self.strings:
            self.check_string(string)
            print()

        return True
      

    def check_string(self, string):
        """
        Checks a single string to see if it is accepted by the PDA
        """
        ret = False

        if self.check_if_in_alphabet(string):
            try:
                print(f"Using string: {string}")
                if self.traverse_table(string):
                    print("String accepted.")
                    ret = True
                else:
                    print("String rejected.")
            except Exception as e:
                print(f"Exception with string {string}: {e}")
                print(traceback.format_exc())

        return ret

    def check_if_in_alphabet(self, string):
        """
        Check each character in the string to make sure it is in the alphabet before testing it
        """
        ret = True

        if len(string) == 0:
            return ret

        for char in string:
            if char in self.alphabet:
                continue
            else:
                print("String contains characters not defined in the alphabet.")
                ret = False
                break

        return ret



    def check_if_start(self, state):
        if state == self.start_state[0]:
            return True
        else:
            return False

    def check_if_end(self, state):
        try:
            if state in self.end_state:
                return True
        except ValueError:
            return False

    def do_stack_action(self, stack_action, curr_stack):
        """
        Checks a node's stack action.
        Will push or pop from the pda's stack.
        """
        if stack_action[0] == stack_action[1]:  # If the action is to do nothing
            return True
        if stack_action[0] == 'E' and stack_action[1] != 'E':  # If the action is to add to the stack
            curr_stack.append(stack_action[1])
            return True
        if stack_action[0] != 'E' and stack_action[1] == 'E':  # If the action is to pop from the stack
            if len(curr_stack) == 0:
                return False
            
            stack_length = len(curr_stack) - 1  # Get the index of the top element of the stack
            if curr_stack[stack_length] == stack_action[0]:
                curr_stack.pop()
                return True
            else:  # The top character of the stack does not meet the requirements to be popped
                return False

        return False


    def traverse(self, current_state, user_string, curr_stack):
        """
        Recursive function that takes the current state to traverse, the current string, and current stack
        and sees if the current state will accept the string. If not, it will call itself again and pass
        in the updated parameters.
        """

        res = False

        if self.print_computation: print(f"Current state: {current_state}, Current stack: {curr_stack}, Current string: \"{user_string}\"")

        if current_state == 0:  # If the state is null, traverse failed
            if self.print_computation: print("Next state is null, failed to traverse.")
            return False
        else:
            for state in current_state.nodes:
                if self.print_computation: print(f"Current state: {state}, Current stack: {curr_stack}, Current string: \"{user_string}\"")
                
                if len(user_string) == 0:  # If the string is empty, see if there is a lambda transition
                    next_state = self.get_transition(state.name, "")
                else:
                    next_state = self.get_transition(state.name, user_string[0])  # Get the next state to travse

                # if self.print_computation: print(f"Next state: {next_state}")

                if self.do_stack_action(state.stack_action, curr_stack):  # If the stack action is successful
                    if state.is_final:  # If the state is final
                        if len(user_string) == 0:  # If the string has been read
                            if len(curr_stack) == 0:  # If the stack has been cleared
                                # if self.print_computation: print(f"Current state: {state}, Current stack: {curr_stack}, Current string: \"{user_string}\"")
                                return True  # Base case, 3 conditions met, the string is accepted.

                    if self.is_lambda:  # If the next state trans. on lambda, don't remove a character
                        res = self.traverse(next_state, user_string, curr_stack)
                        if res:  # Base case, the string is accepted
                            break
                    else:
                        res = self.traverse(next_state, user_string[1:], curr_stack)
                        if res:  # Base case, the string is accepted
                            break
                else:  # If the stack action failed
                    if next_state == 0:
                        if self.print_computation: print("Next state is null, failed to traverse.")
                        return False
                    
                    if next_state.count > 0:  # If there are still potential states to check for an accepting stack action, try them
                        continue
                    else:  # This was the only state to check, therefore it fails to accept the string.
                        return False

                curr_stack = []  # The previous path failed, reset the stack for the next state to traverse

        return res


    def traverse_table(self, user_string):
        """
        Accepts a user's string and recursively traverses the transition table to 
        see if it is accepted by the PDA.
        """
        res = False

        current_state = self.pda_trans_table[1][0]  # Set the initial state to the starting state
        curr_stack = self.pda_stack

        if len(user_string) == 0 and current_state.is_final:
            return True

        # Get the first transition for the initial state
        if (len(user_string) == 0):
            current_state = self.get_transition(current_state.name, "")
        else:
            current_state = self.get_transition(current_state.name, user_string[0])  # Get the next state to travse 

        if self.is_lambda:  # If the next state trans. on lambda, don't remove a character
            res = self.traverse(current_state, user_string, curr_stack)
        else:  # The transition has a character to transition on
            res = self.traverse(current_state, user_string[1:], curr_stack)
        
        self.pda_stack = []
        self.is_lambda = False

        return res


    def get_transition(self, state, char):
        """
        Given a starting state and a character, will return the transition state.
        The transition state is a NodeCollection object, so it could have multiple nodes in it
        """
        # if self.print_computation: print(f"Character trying to traverse on: {char}")

        self.is_lambda = False
        row = self.pda_states.index(state) + 1
        try:
            # get the state index
            col = self.alphabet.index(char) + 1

            trans_state = self.pda_trans_table[row][col]  # Is a node object
        except:  # Catch any potential errors, assume the character was null
            # if self.print_computation: print(f"Character trying to traverse on: {char}")
            trans_state = 0

        # If the character to transition on is empty, check if there is a lambda transition
        if trans_state == 0:
            try:
                col = self.alphabet.index("E") + 1  # Set the column to the lambda column
                trans_state = self.pda_trans_table[row][col]  # Get the transition
                if trans_state != 0:  # If there was a lambda transition
                    self.is_lambda = True
                    if self.print_computation: print(f"Transition is lambda for: {state} to {trans_state}")
            except ValueError:
                pass

        return trans_state

    def construct_trans_table(self, trans_table, row, col, transitions, states):
        """
        Constructs the transition table for the NFA (not t table)
        """
        
        # trans_table[0] is the first row
        # Input the alphabet characters
        trans_table[0][0] = "T"

        # Input the alphabet
        for i in range(len(self.alphabet)):
            trans_table[0][i + 1] = self.alphabet[i]

        # Input the states on the lhs of the table
        for i in range(0, len(states)):
            node = Node()
            node.name = states[i]
            if self.check_if_start(states[i]):
                node.is_start = True
            if self.check_if_end(states[i]):
                node.is_final = True

            trans_table[i + 1][0] = node
            

        # Input the transitions 
        for i in range(len(transitions)):
            transition = transitions[i]  # Take a transition and split it into the start state, character, and end state
            start = transition[0]  # Start state
            char = transition[1]  # Input character
            end = transition[2]  # Transition state from character
            stack_lhs = transition[3]  # Stack character to replace
            stack_rhs = transition[4]  # Character replacing previous stack top

            start_index = states.index(start) + 1
            char_index = self.alphabet.index(char) + 1

            if trans_table[start_index][char_index] == 0:  # If this is an unitialized node
                node_collection = NodeCollection()  # Create a NodeCollection object to store mult. nodes
                node = Node()
                node.name = end
                node.is_transition = True
                if self.check_if_start(end):
                    node.is_start = True
                if self.check_if_end(end):
                    node.is_final = True
                node.stack_action.append(stack_lhs)
                node.stack_action.append(stack_rhs)

                node_collection.add(node)

                trans_table[start_index][char_index] = node_collection  # Add the node to the table
            else:  # If this node already has an existing node, add the next one
                node_collection = NodeCollection()
                node = Node()
                node.name = end
                node.is_transition = True
                if self.check_if_start(end):
                    node.is_start = True
                if self.check_if_end(end):
                    node.is_final = True
                node.stack_action.append(stack_lhs)
                node.stack_action.append(stack_rhs)
                trans_table[start_index][char_index].add(node)

    def print_transition_table(self, trans_table, rows, cols):
        """
        Prints the transition table of the PDA
        """
        for i in trans_table[0]:
            print(f"|{i}".ljust(13, '_'), end="")
        print()

        for r in range(1, rows):
            for c in range(cols):
                    print("|{:11}".format('{}'.format(trans_table[r][c])), end=" ")
            print()

    def parse_data(self):
        """
        Parses the JSON data from the file
        """
        ret = False
        state_len = 0

        # Get the states of the NFA
        try:
            state_len = len(self.input_data['states'])
        except KeyError:
            print("Error: JSON file missing states key/value(s) variable.")
            ret = True
        
        try:
            # Get whether computation will be printed to console
            if self.input_data["show_computation"] == "1":
                self.print_computation = True
            else:
                self.print_computation = False
        except KeyError:
            print("Error: JSON file missing show_computation key/value pair.")
            ret = True

        try:
            for i in range(state_len):
                self.pda_states.append(self.input_data['states'][i])
        except KeyError:
            print("Error: JSON file missing states key/value(s) variable.")
            ret = True

        try:
            # Get the alphabet for the NFA
            alphabet_len = len(self.input_data['alphabet'])

            for i in range(alphabet_len):
                self.alphabet.append(self.input_data['alphabet'][i])
        except KeyError:
            print("Error: JSON file missing alphabet key/value(s) variable.")
            ret = True

        try:
            # Get the start state for the NFA
            self.start_state = self.input_data['start_state']
        except KeyError:
            print("Error: JSON file missing start state key/value pair.")
            ret = True

        try:
            # Get the end state(s)
            end_len = len(self.input_data['end_state'])

            for i in range(end_len):
                self.end_state.append(self.input_data['end_state'][i])
        except KeyError:
            print("Error: JSON file missing end_state key/value(s) variable.")
            ret = True

        try:
            # Get the transitions
            trans_len = len(self.input_data['transitions'])

            for i in range(trans_len):
                self.pda_transitions.append(self.input_data['transitions'][i])
        except:
            print("Error: JSON file missing transitions variable.")
            ret = True

        # Get the strings
        try:
            self.strings = self.input_data['strings']
        except KeyError:
            print("No included strings in JSON file, switching to manual entry mode.")
            self.included_strings = False

        return ret