from queue import Queue
from parser_utils import Item, State, ParsingTable
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
        initial_item = Item(self.grammar.starting_symbol,
                            self.grammar.productions[self.grammar.starting_symbol][0],
                            0)
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

    def create_parsing_table(self):
        states, edges = self.canonical_collection()
        parsing_table = ParsingTable(states, self.grammar.terminals, self.grammar.non_terminals)
        for i in range(parsing_table.nr_rows):
            for j in range(parsing_table.nr_cols):
                if (i, parsing_table.symbols[j]) in edges.keys():
                    parsing_table.goto[i][j] = edges[(i, parsing_table.symbols[j])]
                    parsing_table.action[i] = "s"

            if parsing_table.action[i] == "":
                state = parsing_table.states[i]
                err = True
                for production in state.items:
                    if production.position_for_dot == len(production.right_hand_side):
                        if production.left_hand_side == self.grammar.starting_symbol:
                            parsing_table.action[i] = "acc"
                            err = False
                            break
                        else:
                            idx = self.grammar.productions[production.left_hand_side].index(production.right_hand_side)
                            # reduce, key in grammar.productions, index in list of productions 4 key
                            #                             ^
                            parsing_table.action[i] = "r {} {}".format(production.left_hand_side, idx)
                            err = False
                            break
                if err:
                    parsing_table.action[i] = "err"
        return parsing_table

    def parse(self, string):
        parsing_table = self.create_parsing_table()
        work_stack = ["$", 0]  # Starting state is always the first in this implementation
        input_stack = string.split() + ["$"]
        output = []
        # print("input stack:", input_stack)
        # print("work stack:", work_stack)
        # c_symbol = input_stack[0]
        # c_symbol_idx = parsing_table.symbols.index(c_symbol)

        while True:
            c_state_idx = work_stack[-1]
            if parsing_table.action[c_state_idx] == "acc":
                break
            elif parsing_table.action[c_state_idx] == "s":
                c_symbol = input_stack[0]
                c_symbol_idx = parsing_table.symbols.index(c_symbol)
                if parsing_table.goto[c_state_idx][c_symbol_idx] != -1:
                    work_stack.append(input_stack.pop(0))
                    c_state_idx = parsing_table.goto[c_state_idx][c_symbol_idx]
                    work_stack.append(c_state_idx)

            elif parsing_table.action[c_state_idx][0] == "r":
                r, key, idx = parsing_table.action[c_state_idx].split()
                idx = int(idx)
                c_production = Item(key, self.grammar.productions[key][idx])
                # print("reduce with production:", c_production)
                work_stack = work_stack[:(len(work_stack) - len(c_production.right_hand_side) * 2)]
                c_state_idx = work_stack[-1]
                work_stack.append(c_production.left_hand_side)
                work_stack.append(
                    parsing_table.goto[c_state_idx][parsing_table.symbols.index(c_production.left_hand_side)])
                output.append(c_production)
            else:
                print("ERROR")
                break

            # print("input stack:", input_stack)
            # print("work stack:", work_stack)
            # print("output:", output)

        return output
