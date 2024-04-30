import math
class Node:
    def __init__(self):
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Node({self.children})"


class Leaf:
    def __init__(self, value):
        self.value = value

    def set_value(self, value):
        self.value = value

    def __repr__(self):
        return f"Leaf({self.value})"


def minmax(node_path, is_max, parent):
    current_node = parent
    for index in node_path:
        current_node = current_node.children[index]

    if isinstance(current_node, Leaf):
        return current_node.value

    if is_max:
        return max([minmax(node_path + [i], False, parent) for i in range(len(current_node.children))])

    else:
        return min([minmax(node_path + [i], True, parent) for i in range(len(current_node.children))])


def minmax_alpha_beta(node_path, is_max, parent, alpha):
    current_node = parent
    for index in node_path:
        current_node = current_node.children[index]

    if isinstance(current_node, Leaf):
        return current_node.value

    if is_max:
        return max([minmax(node_path + [i], False, parent) for i in range(len(current_node.children))])

    else:
        return min([minmax(node_path + [i], True, parent) for i in range(len(current_node.children))])


if __name__ == "__main__":
    node = Node()
    node.add_child(Node())
    node.add_child(Node())
    node.children[0].add_child(Leaf(3))
    node.children[0].add_child(Leaf(5))
    node.children[1].add_child(Leaf(2))
    node.children[1].add_child(Leaf(9))
    print(minmax([], False, node))
