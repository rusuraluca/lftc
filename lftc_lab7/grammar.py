class Grammar:
    def __init__(self, filename):
        self.filename = filename

        with open(self.filename, 'r', encoding='utf-8') as file:
            N = set(Grammar.parse_line(file.readline()))
            E = set(Grammar.parse_line(file.readline()))
            S = file.readline().split('=')[1].replace(" ", "").strip()
            file.readline()
            P = Grammar.parse_productions([line.strip() for line in file])
            if not Grammar.validate(N, E, S, P):
                raise Exception(f'Grammar in {filename} is not valid')

            self.non_terminals = N
            self.terminals = E
            self.start_symbol = S
            self.productions = P

    def parse_line(line):
        return line.split('=', maxsplit=1)[1].strip().split()

    def parse_productions(lines):
        P = {}
        for line in lines:
            if line == '':
                continue
            lhs, rhs = line.split('->')
            lhs = lhs.strip()
            rhs_list = rhs.strip().split('|')
            rhs_list = [rhs.strip() for rhs in rhs_list]
            if lhs in P:
                P[lhs].append(rhs_list)
            else:
                P[lhs] = [rhs_list]
        return P

    def validate(N, E, S, P):
        if S not in N:
            return False

        for k, v in P.items():
            if k not in N:
                return False

            for production in v:
                for symbol in production:
                    symbol = symbol.split()
                    for s in symbol:
                        if s not in N and s not in E:
                            print(s)
                            return False

        return True

    def is_cfg(self):
        for key in self.productions.keys():
            if key not in self.non_terminals:
                return False
        return True

    def get_productions_for_non_terminal(self, symbol):
        if symbol in self.terminals:
            raise Exception('Only non-terminals can have productions')
        return self.productions[symbol]

    def get_non_terminals(self):
        return self.non_terminals

    def get_terminals(self):
        return self.terminals

    def get_productions(self):
        return self.productions

    def set_productions(self, productions):
        self.productions = productions

    def get_start_symbol(self):
        return self.start_symbol

    def set_start_symbol(self, start_symbol):
        self.start_symbol = start_symbol

    def get_all_symbols(self):
        return list(self.get_non_terminals()) + list(self.get_terminals())

    def __str__(self) -> str:
        return f"(N)Non-terminals = {self.get_non_terminals()}\n(E)Terminals = {self.get_terminals()}\n(S)Starting symbol = {self.get_start_symbol()}\n(P)Productions = {self.get_productions()}\n"
