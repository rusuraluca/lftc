from grammar import Grammar
from lr0 import LR0Parser

def menu():
    while True:
        print("\n1: Show all terminals")
        print("2: Show all non terminals")
        print("3: Show all productions")
        print("4: Show productions for non terminal")
        print("0: exit")
        com = input("->")
        if com == "0":
            break
        elif com == "1":
            print(grammar.get_terminals())
        elif com == "2":
            print(grammar.get_non_terminals())
        elif com == "3":
            print(grammar.get_productions())
        elif com == "4":
            n_t = input("non terminal: ")
            print(grammar.get_productions_for_non_terminal(n_t))
        else:
            print("Invalid command!")


if __name__ == '__main__':
    grammar = Grammar("g1.txt")
    lr0 = LR0Parser(grammar)
    with open("ccg1.txt", 'w') as f:
        f.write(str(lr0.canonical_collection()))


    grammar = Grammar("g2.txt")
    lr0 = LR0Parser(grammar)
    with open("ccg2.txt", 'w') as f:
        f.write(str(lr0.canonical_collection()))

    grammar = Grammar("g3.txt")
    lr0 = LR0Parser(grammar)
    with open("ccg3.txt", 'w') as f:
        f.write(str(lr0.canonical_collection()))

    menu()
