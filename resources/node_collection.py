from .import node

class NodeCollection:  # NOTE: Add check in add to see if state is final, add bool to set to true
    def __init__(self):
        nodes = []
        self.count = 0

    def add(self, node):
        """
        Adds a node to the nodes list, will increment number of nodes
        """
        self.nodes.append(node)
        # try:
        #     if state not in self.states:  # Check if the state has not been added yet
        #         self.states.append(state)
        #         self.states.sort()  # Sort the list
        #         self.count += 1
        #         return True
        # except ValueError:
        #     pass

    # def __str__(self):
    #     """
    #     Override the string function to call get_formatted_states()
    #     """
    #     if self.is_transition:
    #         return self.name
    #     else:
    #         return self.name + " " + self.stack_action