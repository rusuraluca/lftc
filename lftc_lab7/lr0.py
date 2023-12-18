from typing import Optional
from utils import Production, State
from parsing_table import Action, ParsingTable
from parsing_tree import ParsingTree

class LR0Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.pt: Optional[ParsingTable] = None

    def closure(self, states):
        ans = states[:]
        queue = states[:]
        while len(queue):
            state = queue.pop()
            # print(state)
            potential_non_terminal = state.string_after_point
            for prod in self.grammar.get_productions_for_non_terminal(potential_non_terminal):
                new_state = State(prod, 0)
                if new_state not in ans:
                    queue.append(new_state)
                    ans.append(new_state)
        return ans

    def goto(self, states, term):
        return self.closure([state.shift_dot_right() for state in states if state.string_after_point == term])

    def canonical_collection(self):
        init = self.grammar.starting_symbol
        starting_symbol_state = State(Production("S'", init), 0)

        canonical_collection = []
        goto_dest = {}

        terms = self.grammar.non_terminals
        terms.extend(self.grammar.terminals)

        s0 = self.closure([starting_symbol_state])
        print("s0:", list(map(str, s0)))
        canonical_collection.append(s0)
        i = 0

        while i < len(canonical_collection):
            s = canonical_collection[i]

            for term in terms:
                candidate = self.goto(s, term)
                if len(candidate) == 0:
                    continue

                def add_to_goto_dest(i, term, dest):
                    if i not in goto_dest:
                        goto_dest[i] = {}

                    goto_dest[i][term] = dest

                try:
                    si = canonical_collection.index(candidate)
                    add_to_goto_dest(i, term, si)
                except ValueError:
                    print(f"s{len(canonical_collection)} = goto({i}, {term}) = {list(map(str, candidate))}")
                    add_to_goto_dest(i, term, len(canonical_collection))
                    canonical_collection.append(candidate)

            i += 1

        return canonical_collection, goto_dest

    def construct_parsing_table(self):
        cc, gtd = self.canonical_collection()

        self.pt = ParsingTable(self.grammar)
        self.pt.process_canonical_collection(cc, gtd)

        print(self.pt)

    def parse(self, s):
        if self.pt is None:
            self.construct_parsing_table()
        working_stack = ['$', 0]
        input_stack = [c for c in s] + ['$']
        output_stack = []

        def print_current_state():
            print(f'Work: {working_stack}\t|\t Input: {input_stack}\t|\t Output: {list(map(str, reversed(output_stack)))}')

        while True:
            state_no = working_stack[-1]
            action = self.pt.get_action_for_set(state_no)

            if action == Action.SHIFT or action == Action.REDUCE:
                reduce = False
                if action == Action.SHIFT:
                    print_current_state()
                    next_terminal = input_stack[0]
                    try:
                        print(f'Shifting... current state = {state_no} \t|\t next terminal = {next_terminal} \t|\t '
                            f'goTo = {self.pt.get_goto_destination(state_no, next_terminal)}')
                        next_state_no = self.pt.get_goto_destination(state_no, next_terminal)
                        input_stack.pop(0)
                        working_stack.extend([next_terminal, next_state_no])
                        print()
                    except:
                        reduce = True
                if action == Action.REDUCE or reduce:
                    print_current_state()
                    production = self.pt.get_reduction(state_no)
                    output_stack.append(production)
                    print("Reducing with production", production)

                    rhs_terms = production.rhs.split()
                    while len(rhs_terms):
                        working_stack.pop(-1)
                        cur_term = rhs_terms.pop(-1)
                        if cur_term != working_stack.pop(-1):
                            raise Exception('Action not allowed in reducing.')

                    working_stack.append(production.lhs)
                    print_current_state()
                    last_state = working_stack[-2]
                    last_term = working_stack[-1]
                    print('Adding a state after reduce: state =', last_state, 'term =', last_term)
                    next_state_no = self.pt.get_goto_destination(last_state, last_term)
                    working_stack.append(next_state_no)
                    print()

            else:  # accept
                print_current_state()
                print('Accepting...')
                output_stack.reverse()

                po = ParsingTree()
                po.process_parser_output(output_stack)
                return po