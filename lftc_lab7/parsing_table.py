from enum import Enum
from utils import State, Production
from grammar import Grammar


class Action(Enum):
    SHIFT = 1,
    ACCEPT = 2,
    REDUCE = 3


class ParsingTable:
    def __init__(self, grammar: Grammar) -> None:
        self.table = [] # item structure: action: Action, reduction: production_no, goto: {symbol: stateNo}
        self.grammar: Grammar = grammar

        self.start_production = Production("S'", self.grammar.starting_symbol)
        self.end_state = State(self.start_production, len(str(self.start_production.rhs)))

        self.productions_numbering = grammar.get_productions_list()

    def add_set(self, states_set: set, goto_destinations):
        action = None
        reduction_no = None

        if self.end_state in states_set:
            self.table.append({'action': Action.ACCEPT, 'reduction': None, 'goto': {}})
            return

        for state in states_set:
            if state.string_after_point == '':
                red_no = self.productions_numbering.index(state.prod)

                if action == Action.SHIFT:
                    raise Exception(
                        f'Shift - Reduction Conflict (Set_no:{len(self.table)} - State: {state}, GOTO: ): the grammar is not an LR(0) grammar')
                if action == Action.REDUCE and reduction_no != red_no:
                    print(reduction_no, red_no)
                    raise Exception(
                        f'Reduction - Reduction Conflict (Set_no:{len(self.table)} - State: {state}): the grammar is not an LR(0) grammar')
                action = Action.REDUCE
                reduction_no = red_no
            else:
                action = Action.SHIFT

        self.table.append({'action': action, 'reduction': reduction_no, 'goto': goto_destinations})

    def process_canonical_collection(self, canonical_collection, goto_destinations):
        for i, set in enumerate(canonical_collection):
            self.add_set(set, goto_destinations[i] if i in goto_destinations else {})

    def get_action_for_set(self, state_set_no):
        return self.table[state_set_no]['action']

    def get_goto_destination(self, state_set_no, term):
        return self.table[state_set_no]['goto'][term]

    def get_reduction_number(self, state_set_no):
        return self.table[state_set_no]['reduction']

    def get_reduction(self, state_set_no):
        return self.productions_numbering[self.get_reduction_number(state_set_no)]

    def get_productions_numbering(self):
        return self.productions_numbering

    def __str__(self):
        s = ''
        for i, x in enumerate(self.table):
            s += f"Nr: {i}\t|\taction: {x['action']} {x['reduction'] if x['reduction'] is not None else ''}\t|\t{x['goto']}\n"
        return s