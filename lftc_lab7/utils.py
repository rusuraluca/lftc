class PIFField:
    def __init__(self, key, token_index, table_index) -> None:
        self.key = key
        self.token_index = token_index
        self.table_index = table_index

class PIFReader:
    def __init__(self) -> None:
        self.__pif = []

    def readPIF(self, filename):
        with open(filename, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                key, val = line.split(':')
                val = val.strip('() \n')
                token_index, table_index = val.split(',')
                token_index = int(token_index)
                table_index = int(table_index)

                self.__pif.append(PIFField(key, token_index, table_index))

    def get_keys(self):
        return ['CONST' if x.token_index == 1 else 'IDENT' if x.token_index == 0 else x.key for x in self.__pif]

    def __str__(self) -> str:
        s = ''
        for field in self.__pif:
            s += f'{field.key} -> ({field.token_index}, {field.table_index})\n'

        return s


class State:
    def __init__(self, prod, index):
        self.prod = prod
        self.index = index

    @property
    def string_after_point(self):
        if self.index < len(self.prod.rhs) and self.prod.rhs[self.index] == ' ':
            self.index += 1
        r_index = self.prod.rhs.find(' ', self.index)
        if r_index == -1:
            return self.prod.rhs[self.index:]
        return self.prod.rhs[self.index:r_index]

    def shift_dot_right(self):
        if self.index < len(self.prod.rhs) and self.prod.rhs[self.index] == ' ':
            self.index += 1
        r_index = self.prod.rhs.find(' ', self.index) + 1

        r_index = r_index if r_index != self.index and r_index != 0 else len(self.prod.rhs)
        return State(self.prod, r_index)

    def __str__(self):
        return f"[{self.prod.lhs} -> {self.prod.rhs[:self.index].strip()} . {self.prod.rhs[self.index:].strip()}]"

    def __eq__(self, other):
        return self.prod == other.prod and self.index == other.index


class Production:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return f'{self.lhs} -> {self.rhs}'

    def __eq__(self, other):
        return self.lhs == other.lhs and self.rhs == other.rhs

    def __str__(self):
        return f'{self.lhs} -> {self.rhs}'