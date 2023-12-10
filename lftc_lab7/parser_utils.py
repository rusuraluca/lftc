class ParsingTable:
    def __init__(self, states, terminals, non_terminals):
        self.states = states
        self.nr_rows = len(states)
        self.nr_cols = len(terminals) + len(non_terminals)
        self.goto = [[-1 for _ in range(self.nr_cols)] for _ in range(self.nr_rows)]
        self.action = ["" for _ in range(self.nr_rows)]
        self.symbols = list(terminals) + list(non_terminals)

    def __str__(self):
        string = "Parsing Table:\n"
        string += "{:<4} {:<15} {:<6}\n".format("nr", "action", "goto")
        string += "{:<4} {:<15}".format("", "")
        for i in range(self.nr_cols):
            string += "{:>4}".format(self.symbols[i])
        string += "\n\n"
        for i in range(self.nr_rows):
            string += str("{:<4} {:<15}".format(i, self.action[i]))
            for j in range(self.nr_cols):
                string += "{:>4}".format(self.goto[i][j])
            string += "\n"

        return string

class State:
    def __init__(self, items):
        self.items = items

    def add(self, e):
        self.items.add(e)

    def __str__(self):
        return "State: " + str(self.items)

    def __repr__(self):
        return "\nState: " + str(self.items) + "\n"

    def __eq__(self, other):
        if len(self.items) != len(other.items):
            return False
        if len(self.items.intersection(other.items)) == len(self.items):
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1

class Item:
    def __init__(self, left_hand_side, right_hand_side, position_for_dot=0):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self.position_for_dot = position_for_dot

    def __eq__(self, other):
        if self.position_for_dot == other.position_for_dot and \
                self.left_hand_side == other.left_hand_side and \
                self.right_hand_side == other.right_hand_side:
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.left_hand_side)

    def __str__(self):
        return "Production: {} -> {}; dot: {}".format(self.left_hand_side, self.right_hand_side, self.position_for_dot)

    def __repr__(self):
        return "\nProduction: {} -> {}; dot: {}".format(self.left_hand_side, self.right_hand_side, self.position_for_dot)
