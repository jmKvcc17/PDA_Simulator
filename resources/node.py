

class Node:  # NOTE: Add check in add to see if state is final, add bool to set to true
    def __init__(self):
        self.name = ""
        self.is_final = False
        self.is_start = False
        self.is_transition = False  # If true, __str__ will just return the name
        # Will be used to store what happens to the stack on a state
        # ie. ['E', 'E'] would do nothing to the stack, ['A', 'E'] would pop
        self.stack_action = []  

    # def add(self, state):
    #     """
    #     Adds a state to the states list, will increment number of states
    #     """
    #     try:
    #         if state not in self.states:  # Check if the state has not been added yet
    #             self.states.append(state)
    #             self.states.sort()  # Sort the list
    #             self.count += 1
    #             return True
    #     except ValueError:
    #         pass

    #     return False

    # def get_unformatted_states(self):
    #     """
    #     Returns all states as a single string
    #     """

    #     states = ''
    #     for s in self.states:
    #         states += s
        
    #     return states

    # def check_if_final(self, final_states):
    #     """
    #     Determines whether the node contains a state that is a final state
    #     """
    #     for s in self.states:
    #         try:
    #             if s in final_states:
    #                 return True
    #         except ValueError:
    #             pass
        
    #     return False

    # def get_formatted_states(self):
    #     """
    #     Returns all the states in the node properly formatted.
    #     """
    #     states = "{"

    #     num_states = len(self.states)
    #     for i in range(num_states):
    #         if i < num_states - 1:
    #             states += self.states[i] + ", "
    #         else:
    #             states += self.states[i]

    #     states += "}"

    #     return states

    def __str__(self):
        """
        Override the string function to call get_formatted_states()
        """
        if self.is_transition:
            return self.name
        else:
            return self.name + " " + self.stack_action