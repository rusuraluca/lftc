from grammar import Grammar
from lr0 import LR0Parser


print('\n----------------------------------------------------------------')
g = Grammar('g1.txt')
print(g)
print(f'Is cfg?: {g.is_cfg()}\n')
lr = LR0Parser(g)
print(lr.get_grammar())
lr.write_canonical_collection('ccg1.txt')


print('\n----------------------------------------------------------------')
g = Grammar('g2.txt')
print(g)
print(f'Is cfg?: {g.is_cfg()}\n')
lr = LR0Parser(g)
print(lr.get_grammar())
lr.write_canonical_collection('ccg2.txt')


print('\n----------------------------------------------------------------')
g = Grammar('g3.txt')
print(g)
print(f'Is cfg?: {g.is_cfg()}\n')
lr = LR0Parser(g)
print(lr.get_grammar())
lr.write_canonical_collection('ccg3.txt')
