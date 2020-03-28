import json
from .node import Node
    

class Nfa:
    def __init__(self, data):
        self.input_data = data
        self.strings = []
        # Variables
        # NFA
        self.nfa_states = []
        self.nfa_transitions = []
        self.alphabet = []
        self.end_state = []
        
        # DFA
        self.dfa_states = []
        self.dfa_transitions = []

        # NFA and DFA construction
        self.parse_data()  # Get data from the JSON file

        # NFA construction
        self.nfa_num_rows = len(self.nfa_states) + 1
        self.nfa_num_cols = len(self.alphabet) + 1
        self.nfa_trans_table = [[0 for x in range(self.nfa_num_cols)] for y in range(self.nfa_num_rows)]
        self.construct_trans_table(self.nfa_trans_table, self.nfa_num_rows, self.nfa_num_cols, self.nfa_transitions, self.nfa_states)
        print("---NFA Transition Table---")
        self.print_transition_table(self.nfa_trans_table, self.nfa_num_rows, self.nfa_num_cols)

        # DFA construction
        self.contruct_t_table()  # DFA
        self.dfa_num_rows = len(self.dfa_states) + 1
        self.dfa_num_cols = len(self.alphabet) + 1
        # print(f"Size of  DFA states: {len(self.dfa_states)}")
        # print(f"Number of rows: {self.dfa_num_rows}, number of cols: {self.dfa_num_cols}")
        self.dfa_trans_table = [[0 for x in range(self.dfa_num_cols)] for y in range(self.dfa_num_rows)]  # Init the dfa transition table
        # self.construct_trans_table(self.dfa_trans_table, self.dfa_num_rows, self.dfa_num_cols, self.dfa_transitions, self.dfa_states)
        self.construct_dfa_trans_table(self.dfa_trans_table, self.dfa_num_rows, self.dfa_num_cols, self.dfa_transitions, self.dfa_states)
        self.print_DFA_machine()
        print("---DFA Transition Table---")
        self.print_transition_table(self.dfa_trans_table, self.dfa_num_rows, self.dfa_num_cols)
        self.check_all_strings()

        print("End.")

    def check_all_strings(self):
        print()
        print("---Checking strings---")

        if len(self.strings) == 0:
            print("Error, no strings to check.")
            return

        for s in self.strings:
            self.check_string(self.dfa_trans_table, s)

    # Checks if a string is valid or not
    def check_string(self, trans_table, user_string):
        print(f"Checking string: {user_string}")

        curr_state = self.dfa_trans_table[1][0]

        has_state = True

        for char in user_string:
            curr_state = self.temp_get_transition(self.dfa_trans_table, self.dfa_states, curr_state, char)
            # print(f"Returned state: {curr_state}")
            if curr_state == 0:
                has_state = False
                break

        if (has_state):
            if curr_state.check_if_final(self.end_state):
                print("String accepted.")
            else:
                print("String not accepted.")
        else:
            print("String not accepted")
                

    # Parses the JSON data from the file
    def parse_data(self):
        # Get the states of the NFA
        state_len = len(self.input_data['states'])

        for i in range(state_len):
            self.nfa_states.append(self.input_data['states'][i])

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
            self.nfa_transitions.append(self.input_data['transitions'][i])

        # Get the strings
        self.strings = self.input_data['strings']
        # print(self.strings)

    def construct_dfa_trans_table(self, trans_table, row, col, transitions, states):
        trans_table[0][0] = "T"

        for i in range(len(self.alphabet)):
            trans_table[0][i + 1] = self.alphabet[i]

        # Input the states
        for i in range(len(states)):
            trans_table[i + 1][0] = states[i]

        # Input the transitions 
        for i in range(len(transitions)):
            transition = transitions[i]  # Take a transition and split it into the start state, character, and end state
            start = transition[0]
            char = transition[1]
            end = transition[2]

            i = 1
            for s in states:
                # print(f"Comparing: {start}, {s}")
                if start == s:
                    break
                i += 1

            # start_index = states.index(start) + 1
            row_index = i
            col_index = self.alphabet.index(char) + 1

            trans_table[row_index][col_index] = end

    # Constructs the transition table for the NFA (not t table)
    def construct_trans_table(self, trans_table, row, col, transitions, states):
        # self.nfa_num_rows = len(self.nfa_states) + 1
        # self.nfa_num_cols = len(self.alphabet) + 1
        # self.nfa_trans_table = [[0 for x in range(self.nfa_num_cols)] for y in range(self.nfa_num_rows)]

        # trans_table[0] is the first row
        # Input the alphabet characters
        trans_table[0][0] = "T"

        for i in range(len(self.alphabet)):
            trans_table[0][i + 1] = self.alphabet[i]

        # Input the states
        for i in range(len(states)):
            node = Node()
            node.add(states[i])
            trans_table[i + 1][0] = node

        # Input the transitions 
        for i in range(len(transitions)):
            transition = transitions[i]  # Take a transition and split it into the start state, character, and end state
            start = transition[0]
            char = transition[1]
            end = transition[2]

            start_index = states.index(start) + 1
            char_index = self.alphabet.index(char) + 1

            if trans_table[start_index][char_index] == 0:  # If this is an unitialized node
                node = Node()
                trans_table[start_index][char_index] = node  # Create the node object
                trans_table[start_index][char_index].add(end)  # Add the state to the node
            else:
                # self.nfa_trans_table[start_index][char_index] += end 
                trans_table[start_index][char_index].add(end)  # There is already a state in this node, add to it

    # Another temp function since I wrote myself into a corner
    def temp_get_transition(self, trans_table, states, state, char):
        row = 1
        for s in states:
            # print(f"State: {state}.")
            if s.states == state.states:
                # print(f"Found at index {row}")
                break
            row += 1

        # row = states.index(state) + 1
        col = self.alphabet.index(char) + 1

        return trans_table[row][col]


    def get_transition(self, trans_table, states, state, char):
        # get the state index
        row = states.index(state) + 1
        col = self.alphabet.index(char) + 1

        trans_state = trans_table[row][col]  # Is a node object

        # print(f"trans({state}, {char}) = {trans_state}")

        return trans_state
        

    def contruct_t_table(self):
        # print("--Constructing T Table--")

        # Create a temp node object for the start state.
        node = Node()
        node.add(self.start_state[0])

        # Add start state to Q'
        # self.dfa_states.append(self.start_state[0])
        self.dfa_states.append(node)

        temp_states = []  # Will hold states for the duration of the while loop. Once it has no states, the NFA has been traveled
        trans_state = []
        temp_transition = []
        # temp_states.append(self.start_state[0])
        temp_states.append(node)

        while len(temp_states) != 0:  # Loop until there are no new states left

            current_state = temp_states.pop()

            for char in self.alphabet:  # Try each character in the alphabet
                if current_state.count == 1:  # If only one state
                    trans_state = self.single_state_transition(current_state, char)
                elif current_state.count > 1:  # If there are multiple states
                    trans_state = self.mult_state_transition(current_state, char)  # Process multi state transitions  
                else:  # Empty state
                   print(f"Empty state: {current_state}")
                   continue  # Skip to next state

                if trans_state.count == 0:  # Skip states that don't have a transition for a character
                    continue

                # Create the transition
                # temp_transition.append(current_state.get_unformatted_states())  # Append the start state
                temp_transition.append(current_state)  # Append the start state
                temp_transition.append(char)  # Append the character
                # temp_transition.append(trans_state.get_unformatted_states())  # Append the transition state
                temp_transition.append(trans_state)
                self.dfa_transitions.append(temp_transition)
                temp_transition = []

                if self.check_if_state_in_dfa_states(trans_state) == False:  # Check if the state is in the global and temp states list
                    self.dfa_states.append(trans_state)
                    temp_states.append(trans_state)
        
        # print(f"DFA States: ", end=" ")
        # for s in self.dfa_states:
        #     print(f"{s.states}", end=" ")
        
        print()

        # print(f"DFA Transitions: ")
        # for t in self.dfa_transitions:
        #     print(f"{t}")
        

    # Check if a node (state) is already in dfa_states
    def check_if_state_in_dfa_states(self, state):
        for s in self.dfa_states:
            if state.states == s.states:
                return True

        return False


    def single_state_transition(self, state, char):
        # print("--Single state transitions")
        combined_state = []

        # trans_state = self.get_transition(state.states[0], char)  # Get the transition for the state
        trans_state = self.get_transition(self.nfa_trans_table, self.nfa_states, state.states[0], char)
        if trans_state != 0:  # If the transition is not null
            for s in trans_state.states:
                combined_state.append(s)

        # Get the unique values for the list and sort
        combined_state = list(set(combined_state))
        combined_state.sort()
        
        # print(f"Combined state: {combined_state}")

        # Combine combined_state into a node
        node = Node()
        for n in combined_state:
            node.add(n)

        # print(f"-New node: {node}")

        return node


    def mult_state_transition(self, states, char):
        # print("**Multiple state transitions")
        # print(f"Current State: {states}, Current character: {char}")

        combined_state = []
        for state in states.states:  # split the multiple states up and test their transitions, will combine later
            # trans_state = self.get_transition(state, char)
            trans_state = self.get_transition(self.nfa_trans_table, self.nfa_states, state, char)
            if trans_state != 0:
                # combined_state.append(trans_state)
                for s in trans_state.states:
                    combined_state.append(s)
        
        # Get the unique values for the list and sort
        combined_state = list(set(combined_state))
        combined_state.sort()
        # print(f"Combined state: {combined_state}")

        # Combine combined_state into a node
        node = Node()
        for n in combined_state:
            node.add(n)

        # print(f"-New node: {node}")

        return node

    def print_DFA_machine(self):
        print("States in M':", end=" ")
        for s in self.dfa_states:
            print(s, end=" ")
        print()

        print("Alphabet of M': ", end=" ")
        for s in self.alphabet:
            print(s, end=" ")
        print()

        print("Transitions of M': ")
        for r in self.dfa_transitions:
            for c in r:
                print(c, end=" ")
            print()

        print(f"Start state of M': {self.start_state}")
        print(f"Acceptign state of M': {self.end_state}")
        
    def print_transition_table(self, trans_table, rows, cols):
        for i in trans_table[0]:
            print(f"|{i}".ljust(15, '_'), end="")
        print()

        for r in range(1, rows):
            for c in range(cols):
                if r == 1 and c == 0:
                    print("|->{:11}".format('{}'.format(trans_table[r][c])), end=" ")
                    continue
                if c == 0 and trans_table[r][c].check_if_final(self.end_state) == True:
                    print("|*{:12}".format('{}'.format(trans_table[r][c])), end=" ")
                else:
                    print("|{:13}".format('{}'.format(trans_table[r][c])), end=" ")
            print()