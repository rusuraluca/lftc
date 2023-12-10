from queue import Queue
from parser_utils import Item, State
from copy import deepcopy


class LR0Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.enrich_grammar()
        self.states = []

    def enrich_grammar(self):
        P = self.grammar.get_productions()
        enrich_start_symbol = 'S0'
        P[enrich_start_symbol] = [[self.grammar.get_starting_symbol()]]
        self.grammar.set_starting_symbol(enrich_start_symbol)
        self.grammar.set_productions(P)

    def get_non_terminal_preceded_by_dot(self, item):
        try:
            rhs = item.get_right_hand_side()
            if item.get_position_for_dot() < len(rhs):
                term = rhs[item.get_position_for_dot()]
                if term in self.grammar.get_non_terminals():
                    return term
        except Exception as err:
            print("Error: ", err)
        return None

    def closure(self, items):
        closure = set(items)
        pending = Queue()
        for item in items:
            pending.put(item)
        while not pending.empty():
            current_item = pending.get()
            if current_item.position_for_dot < len(current_item.right_hand_side):
                lhs = current_item.right_hand_side[current_item.position_for_dot]
                if lhs in self.grammar.non_terminals:
                    for rhs in self.grammar.productions[lhs]:
                        prod = Item(lhs, rhs, 0)
                        if prod not in closure:
                            closure.add(prod)
                            pending.put(prod)
        return closure

    def goto(self, state, item):
        new_state = []
        for production in state:
            if production.position_for_dot < len(production.right_hand_side) and production.right_hand_side[production.position_for_dot] == item:
                production.position_for_dot += 1
                new_state.append(production)
        return self.closure(new_state)

    def canonical_collection(self):
        initial_item = Item(self.grammar.starting_symbol, self.grammar.productions[self.grammar.starting_symbol][0])
        states = [State(self.closure([initial_item]))]
        index = -1
        edges = {}
        while index < len(states) - 1:
            index += 1
            state = states[index]
            for symbol in self.grammar.get_all_symbols():
                goto_productions = []
                for production in state.items:
                    if production.position_for_dot < len(production.right_hand_side) and \
                            production.right_hand_side[production.position_for_dot] == symbol:
                        goto_productions.append(deepcopy(production))
                    if len(goto_productions):
                        goto = self.goto(goto_productions, symbol)
                        if len(goto) != 0:
                            if State(goto) not in states:
                                states.append(State(goto))
                                edges[(index, symbol)] = len(states) - 1
                            else:
                                edges[(index, symbol)] = states.index(State(goto))
        return states, edges
