
class Leaf:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "("+self.value+")"



class Node:
    def __init__(self, value):
        self.value = value
        self.children = {} #{branch:value}

    def add_children(self, obj, branch):
        self.children[branch] = obj
        
    def __str__(self):
        node_str = "["+self.value+":]"
        for branch, obj in self.children.items():
            node_str = node_str[:-1]
            node_str += str(branch)+"->"+str(obj)+"]"
        return node_str
    
class DecisionTree:
    def __init__(self):
        self.root = None
        self.nodes = {}
        self.leaves = {}

    def new_node(self, parent, value, branch):
        new_node = Node(value)
        if self.root is None:
            self.root = new_node
        self.nodes[value] = new_node
        if parent != 'root':
            self.nodes[parent].add_children(new_node, branch)
    
    def add_node(self, parent, node, branch):
        if self.root is None:
            self.root = node
        self.nodes[node.value] = node
        if parent != 'root':
            self.nodes[parent].add_children(node, branch)


    def add_leaf(self, parent, value, branch):
        new_leaf = Leaf(value)
        if self.root is None:
            self.root = new_leaf
        self.leaves[branch] = new_leaf
        if parent != 'root':
            self.nodes[parent].add_children(new_leaf, branch)

    def __str__(self):
        if self.root is None:
            return "[Empty Tree]"
        return str(self.root)
