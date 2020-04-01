import json
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
        # Used to check if the current transition was a lambda transition, as to not 
        # consume a character in the string
        self.is_lambda = False
        self.included_strings = True  # Bool to check if the included JSON file has strings provided

        # NFA and DFA construction
        self.parse_data()  # Get data from the JSON file

        # NFA construction
        self.pda_num_rows = len(self.pda_states) + 1
        self.pda_num_cols = len(self.alphabet) + 1
        self.pda_trans_table = [[0 for x in range(self.pda_num_cols)] for y in range(self.pda_num_rows)]
        self.construct_trans_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols, self.pda_transitions, self.pda_states)
        self.print_transition_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols)

        # self.pda_stack.append('A')
        # print(self.do_stack_action(['E', 'E']))
        # print(self.pda_stack)
        # print(self.do_stack_action(['E', 'A']))
        # print(self.pda_stack)
        # print(self.do_stack_action(['A', 'E']))
        # print(self.pda_stack)
        # print(self.do_stack_action(['B', 'E']))
        # print(self.pda_stack)

        if self.traverse_table("0011"):
            print("String accepted.")
        else:
            print("String rejected.")

        print("End.")

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

    def do_stack_action(self, stack_action):
        """
        Checks a node's stack action.
        Will push or pop from the pda's stack.
        """
        if stack_action[0] == 'E' and stack_action[1] == 'E':  # If the action is to do nothing
            return True
        if stack_action[0] == 'E' and stack_action[1] != 'E':  # If the action is to add to the stack
            self.pda_stack.append(stack_action[1])
            return True
        if stack_action[0] != 'E' and stack_action[1] == 'E':  # If the action is to pop from the stack
            if len(self.pda_stack) == 0:  # If the length of the stack is zero, then the action fails
                return False
            
            stack_length = len(self.pda_stack) - 1  # Get the index of the top element of the stack
            if self.pda_stack[stack_length] == stack_action[0]:  # If the top character of the stack matches
                self.pda_stack.pop()  # Remove the character from the stack
                return True
            else:
                return False


    def traverse_table(self, user_string):
        # user_string = "0011"
        traverse_table_bool = True  # Used for while loop to traverse the PDA
        user_string_index = 0
        user_string_length = len(user_string)
        ret = False

        current_state = self.pda_trans_table[1][0]  # Set the initial state to the starting state
        temp_states = []  # Used when a state has multiple states to potentially transition on

        # print(current_state)

        # Get the first transition from the starting state
        current_char = user_string[user_string_index]
        current_state = self.get_transition(current_state.name, current_char)

        while(traverse_table_bool):
            if current_state == 0:  # Check if the state is empty on a character
                print("Encountered character that cannot be accepted at a state.")
                # traverse_table_bool = False
                break
            else:  # There is a transition on that character
                if self.is_lambda:  # If the last transition was a lambda transition
                    for node in current_state.nodes:
                        print(node)
                        temp_states.append(node)
                else:  # It was not a lambda transition

            break

            # current_char = user_string[user_string_index]
            # if self.is_lambda:  # If the last transition was a lambda transition
            #     for state in current_state

            # current_state = self.get_transition(current_state.name, current_char)

            if current_state == 0:  # Check if the state is empty on a character
                print("Encountered character that cannot be accepted at a state.")
                # traverse_table_bool = False
                break
            # if current_state.count > 2:  # If this is a mult. state transition
        
        return ret


    def get_transition(self, state, char):
        """
        Given a starting state and a character, will return the transition state.
        The transition state is a NodeCollection object, so it could have multiple nodes in it
        """
        self.is_lambda = False

        # get the state index
        row = self.pda_states.index(state) + 1
        col = self.alphabet.index(char) + 1

        trans_state = self.pda_trans_table[row][col]  # Is a node object

        # If the character to transition on is empty, check if there is a lambda transition
        if trans_state == 0:
            col = self.alphabet.index("E") + 1
            trans_state = self.pda_trans_table[row][col]
            self.is_lambda = True

        return trans_state

    # Constructs the transition table for the NFA (not t table)
    def construct_trans_table(self, trans_table, row, col, transitions, states):
        
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
        for i in trans_table[0]:
            print(f"|{i}".ljust(13, '_'), end="")
        print()

        for r in range(1, rows):
            for c in range(cols):
                    print("|{:11}".format('{}'.format(trans_table[r][c])), end=" ")
            print()

    # Parses the JSON data from the file
    def parse_data(self):
        # Get the states of the NFA
        state_len = len(self.input_data['states'])

        for i in range(state_len):
            self.pda_states.append(self.input_data['states'][i])

        # Get the alphabet for the NFA
        alphabet_len = len(self.input_data['alphabet'])

        for i in range(alphabet_len):
            self.alphabet.append(self.input_data['alphabet'][i])

        # Get the start state for the NFA
        self.start_state = self.input_data['start_state']

        # Get the end state(s)
        end_len = len(self.input_data['end_state'])

        for i in range(end_len):
            self.end_state.append(self.input_data['end_state'][i])

        # Get the transitions
        trans_len = len(self.input_data['transitions'])

        for i in range(trans_len):
            self.pda_transitions.append(self.input_data['transitions'][i])

        # Get the strings
        try:
            self.strings = self.input_data['strings']
        except KeyError:
            print("No included strings in JSON file, switching to manual entry mode.")
            self.included_strings = False