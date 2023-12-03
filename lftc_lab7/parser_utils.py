class CanonicalCollection:
    def __init__(self, states=None, adjacency_list=None):
        self.states = states or []
        self.adjacency_list = adjacency_list or {}

    def add_state(self, state):
        self.states.append(state)

    def get_states(self):
        return self.states

    def get_adjacency_list(self):
        return self.adjacency_list

    def __len__(self):
        return len(self.states)

    def __str__(self):
        return '\n'.join([str(state) for state in self.states])


class State:
    def __init__(self, items):
        self.items = items

    def get_items(self):
        return self.items

    def get_symbols_succeeding_the_dot(self):
        symbols = set()
        for item in self.items:
            if item.get_position_for_dot() < len(item.get_right_hand_side()):
                symbols.add(item.get_right_hand_side()[item.get_position_for_dot()])
        return symbols

    def __str__(self):
        items = '\n '.join([str(item) for item in self.items])
        return f"State:\n {items}"


class Item:
    def __init__(self, left_hand_side, right_hand_side, position_for_dot):
        self.left_hand_side = left_hand_side
        self.right_hand_side = right_hand_side
        self.position_for_dot = position_for_dot

    def get_left_hand_side(self):
        return self.left_hand_side

    def get_right_hand_side(self):
        return self.right_hand_side

    def get_position_for_dot(self):
        return self.position_for_dot

    def __str__(self):
        return f"Item: {self.left_hand_side} -> {self.right_hand_side}, dot - {self.position_for_dot}"
