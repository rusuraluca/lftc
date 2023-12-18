from utils import Production
from collections import deque


class Node:
    next_id = 0

    def __init__(self, child, right_sibling, value, depth):
        self.child: Node = child
        self.right_sibling: Node = right_sibling
        self.value = value
        self.depth = depth
        self.id = Node.next_id
        Node.next_id += 1

    def get_child(self):
        return self.child

    def set_child(self, val):
        self.child = val

    def get_right_sibling(self):
        return self.right_sibling

    def set_right_sibling(self, val):
        self.right_sibling = val

    def get_value(self):
        return self.value

    def set_value(self, val):
        self.value = val

    def get_depth(self):
        return self.depth

    def set_depth(self, val):
        self.depth = val

    def __str__(self) -> str:
        return f"{self.value}(id: {self.id}, child: { self.child.id if self.child else '-'}, " \
            f"right id: {self.right_sibling.id  if self.right_sibling else '-'}, depth: {self.depth})"


class ParsingTree:
    def __init__(self) -> None:
        self.head = None

    def search_parent(self, node: Node, value):
        if node.right_sibling:
            obtained = self.search_parent(node.right_sibling, value)
            if obtained:
                return obtained
        if node.value == value and node.child is None:
            return node
        if node.child:
            obtained = self.search_parent(node.child, value)
            if obtained:
                return obtained
        return None

    def add_production(self, production: Production):
        parent = production.lhs
        children = production.rhs.split()
        print(f"Parent: {parent}, children: {children}")
        parent = self.search_parent(self.head, parent) if self.head is not None else Node(None, None, parent, 0)
        self.head = parent if self.head is None else self.head

        right_sibling = None
        for i in range(len(children) - 1, -1, -1):
            right_sibling = Node(None, right_sibling, children[i], parent.depth + 1)
        parent.child = right_sibling

    def process_parser_output(self, production_list):
        for production in production_list:
            self.add_production(production)

    def print_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))
        f.close()

    def __str__(self) -> str:
        s = ''
        q = deque()
        q.append(self.head)
        while len(q):
            node = q.pop()
            s += str(node) + '\n'
            if node.right_sibling:
                q.append(node.right_sibling)
            if node.child:
                q.append(node.child)
        return s
