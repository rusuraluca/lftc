from utils import Production
from functools import reduce


class Grammar:
    def __init__(self):
        self.non_terminals = set()
        self.terminals = set()
        self.starting_symbol = ''
        self.productions = {}
        self.cfg = True

    def read_from(self, filename: str):
        f = open(filename, 'r')
        lines = f.readlines()

        non_terminals = self.parse_line(lines[0])
        terminals = self.parse_line(lines[1])
        starting_symbol = lines[2].split('=')[1].replace(" ", "").strip()
        productions = lines[4:]

        self.terminals = terminals
        self.non_terminals = non_terminals
        self.starting_symbol = starting_symbol

        for prod_line in productions:
            if len(prod_line.strip()):
                self.process_production_line(prod_line)

    def parse_line(self, line):
        return line.split('=', maxsplit=1)[1].strip().split()

    def process_production_line(self, prod_line: str):
        non_terminal, rhp = list(map(lambda s: s.strip(), prod_line.split('->')))
        if non_terminal not in self.non_terminals:
            print('Not CFG: NON TERMINAL: ' + non_terminal)
            exit(0)

        for rule in list(map(lambda s: s.strip(), rhp.split('|'))):
            production = Production(non_terminal, rule)
            if non_terminal in self.productions:
                self.productions[non_terminal].append(production)
            else:
                self.productions[non_terminal] = [production]

    def get_productions_for_non_terminal(self, symbol):
        if symbol in self.terminals or symbol not in self.productions:
            return []
        return self.productions[symbol]

    def get_non_terminals(self):
        return sorted(self.non_terminals)

    def get_terminals(self):
        return sorted(self.terminals)

    def get_productions(self):
        return self.productions

    def set_productions(self, productions):
        self.productions = productions

    def get_productions_list(self):
        return list(
            reduce(lambda acc, key: acc + self.productions[key],
                self.productions,
                [],
                )
        )

    def get_str_productions(self):
        productions = reduce(lambda acc, cur: acc + '\n' + str(list(map(str, cur[1]))), self.get_productions().items(), '')
        return productions

    def get_starting_symbol(self):
        return self.starting_symbol

    def set_starting_symbol(self, starting_symbol):
        self.starting_symbol = starting_symbol

    def get_all_symbols(self):
        return list(self.get_non_terminals()) + list(self.get_terminals())

    def is_cfg(self):
        return self.cfg

    def __str__(self) -> str:
        return f"(N)Non-terminals = {self.get_non_terminals()}\n(E)Terminals = {self.get_terminals()}\n(S)Starting symbol = {self.get_starting_symbol()}\n(P)Productions = {self.get_str_productions()}\n"
