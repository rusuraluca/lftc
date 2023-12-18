from grammar import Grammar
from lr0 import LR0Parser
from utils import PIFReader


def menu():
    grammar.read_from("input/g1.txt")
    print(grammar)
    while True:
        print("\n1: Show all terminals")
        print("2: Show all non terminals")
        print("3: Show all productions")
        print("4: Show productions for non terminal")
        print("5: Is CFG grammar")
        print("0: exit")
        com = input("->")
        if com == "0":
            break
        elif com == "1":
            print(grammar.get_terminals())
        elif com == "2":
            print(grammar.get_non_terminals())
        elif com == "3":
            print(grammar.get_str_productions())
        elif com == "4":
            n_t = input("Non terminal: ")
            print(grammar.get_productions_for_non_terminal(n_t))
        elif com == "5":
            print(grammar.is_cfg())
        else:
            print("Invalid command!")


grammar = Grammar()


if __name__ == '__main__':
    grammar.read_from("input/g1.txt")
    lr0 = LR0Parser(grammar)
    lr0.construct_parsing_table()
    seq = ""
    with open("input/seq.txt", 'r') as f:
        for line in f.readlines():
            line = line.strip()
            seq += line
    po = lr0.parse(seq)
    po.print_to_file(f'output/g1.out')

    grammar.read_from("input/g2.txt")
    lr0 = LR0Parser(grammar)
    lr0.construct_parsing_table()
    pr = PIFReader()
    pr.readPIF(f'input/PIF.txt')
    po = lr0.parse(pr.get_keys())
    po.print_to_file(f'output/g2.out')

    menu()
