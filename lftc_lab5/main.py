from grammar import Grammar


g = Grammar.from_file('g1.txt')
print(g)
print(g.get_nonterminal_productions('S'))
print(g.is_cfg())


g = Grammar.from_file('g2.txt')
print(g)
print(g.get_nonterminal_productions('assignStmt'))
print(g.is_cfg())


g = Grammar.from_file('g3.txt')
print(g)
print(g.get_nonterminal_productions('A'))
print(g.is_cfg())