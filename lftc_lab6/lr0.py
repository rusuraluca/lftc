from grammar import Grammar
from parser_utils import CanonicalCollection, Item, State


class LR0Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.productions = []
        self.enrich_grammar()

    def enrich_grammar(self):
        P = self.grammar.get_productions()
        enrich_start_symbol = 'S0'
        P[enrich_start_symbol] = [[self.grammar.get_start_symbol()]]
        self.grammar.set_start_symbol(enrich_start_symbol)
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

    def closure(self, item):
        closure_items = {item}
        pending = [item]

        while pending:
            current_item = pending.pop()
            non_terminal = self.get_non_terminal_preceded_by_dot(current_item)
            if non_terminal in self.grammar.get_non_terminals():
                for prod in self.grammar.get_productions_for_non_terminal(non_terminal):
                    new_item = Item(non_terminal, prod, 0)
                    if new_item not in closure_items:
                        closure_items.add(new_item)
                        pending.append(new_item)
        return State(list(closure_items))

    def go_to(self, state, item):
        result = set()

        for i in state.get_items():
            try:
                rhs = i.get_right_hand_side()
                if i.get_position_for_dot() < len(rhs):
                    symbol_at_dot = rhs[i.get_position_for_dot()]
                    if symbol_at_dot == item:
                        next_item = Item(i.get_left_hand_side(), i.get_right_hand_side(), i.get_position_for_dot() + 1)
                        new_state = self.closure(next_item)
                        result.update(new_state.get_items())
            except Exception as err:
                print("Error: ", err)

        return State(result)

    def canonical_collection(self):
        canonical_collection = CanonicalCollection()

        initial_item = Item(
            self.grammar.get_start_symbol(),
            self.grammar.get_productions_for_non_terminal(self.grammar.get_start_symbol())[0],
            0
        )
        initial_state = self.closure(initial_item)
        canonical_collection.add_state(initial_state)
        visited_states = set()

        index = 0
        while index < len(canonical_collection.get_states()):
            state = canonical_collection.get_states()[index]
            visited_states.add(state)
            for symbol in state.get_symbols_succeeding_the_dot():
                new_state = self.go_to(state, symbol)
                if len(new_state.get_items()) != 0 and new_state not in visited_states:
                    canonical_collection.add_state(new_state)
            index += 1
        return canonical_collection

    def get_grammar(self):
        return self.grammar

    def write_canonical_collection(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.canonical_collection()))