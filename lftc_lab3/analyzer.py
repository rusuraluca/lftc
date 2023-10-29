from enum import Enum
import re
from symboltables import SymbolTableConstants, SymbolTableIdentifiers


class TokenTypes(Enum):
    RESERVED_WORD = 1
    SEPARATOR = 2
    OPERATOR = 3
    IDENTIFIER = 4
    CONSTANT = 5
    
    
class LexicalAnalyzer:
    def __init__(self, filename, token_file):
        self.filename = filename
        self.token_file = token_file
        self.constant_table = SymbolTableConstants()
        self.identifiers_table = SymbolTableIdentifiers()
        self.pif = []
        self.reserved_words = []
        self.operators = []
        self.separators = []
        self.get_tokens()
        self.constants_count = 0

    def scan_file(self):
        with open(self.filename, 'r') as program:
            line_count = 0
            for line in program:
                line_count += 1
                line = line.replace('\n', '')
                operators_and_separators = '(==|=|!=|\+=|-=|\*=|\/=|<=|>=|[\+\-\*=\/<>!;\[\]\{\}\(\),;]|\|\||&&)'
                
                for word_with_sep_and_op in line.split():
                    for word in re.split(operators_and_separators, word_with_sep_and_op):
                        if word == '':
                            continue
                        
                        if word in self.reserved_words or word in self.operators or word in self.separators:
                            self.pif.append((word, 0))
                            
                        elif self.is_identifier(word):
                            if self.identifiers_table.get_position(word) is None:
                                self.identifiers_table.add_identifier(word, None)
                            self.pif.append((TokenTypes.IDENTIFIER, self.identifiers_table.get_position(word)))
                            
                        elif self.is_constant(word):
                            if self.constant_table.get_position(word) is None:
                                self.constant_table.add_constant(self.constants_count, word)
                                self.constants_count += 1
                            self.pif.append((TokenTypes.CONSTANT, self.constant_table.get_position(self.constants_count - 1)))
                            
                        else:
                            print(f'Lexical error at line {line_count}')
                            return
                        
            print('Lexically correct')
            
        with open('ST.out', 'w') as output:
            print(str(self.identifiers_table.symboltable))
            output.write(str(self.identifiers_table.symboltable))
            
        with open('PIF.out', 'w') as output:
            for key, value in self.pif:
                output.write(f"{key} - {value}\n")

    def get_tokens(self):
        should_add_in = TokenTypes.RESERVED_WORD
        with open(self.token_file, 'r') as token_file:
            for line in token_file:
                line = line.replace('\n', '')

                if line == '[reserved_words]':
                    continue
                
                if line == '[operators]':
                    should_add_in = TokenTypes.OPERATOR
                    continue
                
                if line == '[separators]':
                    should_add_in = TokenTypes.SEPARATOR
                    continue
                
                if should_add_in == TokenTypes.RESERVED_WORD:
                    self.reserved_words.append(line)
                    
                if should_add_in == TokenTypes.OPERATOR:
                    self.operators.append(line)
                    
                if should_add_in == TokenTypes.SEPARATOR:
                    self.separators.append(line)

    def is_identifier(self, string):
        if string[0] != '_':
            return False
    
        for char in string[1:]:
            if not char.isalnum() and char != '_':
                return False
            
        return True
    
    def is_constant(self, string):
        if string[0] == '0' and len(string) > 1:
            return False
        
        if string[0] == '0' and len(string) == 1:
            return True
        
        if string[0] == '-' and len(string) > 1:
            string = string[1:]
            
        for char in string:
            if not char.isdigit():
                return False
            
        return True