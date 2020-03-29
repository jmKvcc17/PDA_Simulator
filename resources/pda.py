import json
from .node import Node
from .node_collection import NodeCollection

class PDA:
    def __init__(self, data):
        self.input_data = data
        self.strings = []

        # Variables
        # NFA
        self.pda_states = []
        self.pda_transitions = []
        self.alphabet = []
        self.end_state = []
        self.pda_stack = [] # Use append() to push, pop() to remove

        # NFA and DFA construction
        self.parse_data()  # Get data from the JSON file

        # NFA construction
        self.pda_num_rows = len(self.pda_states) + 1
        self.pda_num_cols = len(self.alphabet) + 1
        self.pda_trans_table = [[0 for x in range(self.pda_num_cols)] for y in range(self.pda_num_rows)]
        self.construct_trans_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols, self.pda_transitions, self.pda_states)
        self.print_transition_table(self.pda_trans_table, self.pda_num_rows, self.pda_num_cols)
        print(self.get_transition(self.pda_trans_table, self.pda_states, "q3", "E"))
        # self.print_transition_table(self.nfa_trans_table, self.nfa_num_rows, self.nfa_num_cols)
        # self.check_all_strings()

        print("End.")

    def check_if_start(self, state):
        if state == self.start_state:
            return True
        else:
            return False

    def check_if_end(self, state):
        try:
            if state in self.end_state:
                return True
        except ValueError:
            return False

    # def traverse_table(self):

    def get_transition(self, trans_table, states, state, char):
        """
        Given a starting state and a character, will return the transition state.
        The transition state is a NodeCollection object, so it could have multiple nodes in it
        """
        # get the state index
        row = states.index(state) + 1
        col = self.alphabet.index(char) + 1

        trans_state = trans_table[row][col]  # Is a node object

        # print(f"trans({state}, {char}) = {trans_state}")

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

                node_collection.add(node)

                trans_table[start_index][char_index] = node_collection  # Create the node object
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
        self.strings = self.input_data['strings']
        # print(self.strings)