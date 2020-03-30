

class Node:  
    """
    Represents a single node in the transition table. Will hold the node's name (ie. q1, q2, etc).
    Has properties to determine if it is a terminal state, start state, or is a transition.
    Each state in a PDA needs to store what action the stack will perform, which is stored in stack_action
    """
    def __init__(self):
        self.name = ""
        self.is_final = False
        self.is_start = False
        self.is_transition = False  # If true, __str__ will return the name and the stack action
        # Will be used to store what happens to the stack on a state
        # ie. ['E', 'E'] would do nothing to the stack, ['A', 'E'] would pop
        self.stack_action = []  

    def __str__(self):
        """
        Override the string function to call get_formatted_states()
        """
        if self.is_transition:
            return self.name + " " + self.stack_action[0] + self.stack_action[1]
        else:
            string = self.name
            if self.is_start:
                string = "->" + string
            if self.is_final:
                string = "*" + string
            
            return string