from .Edge import *
from .Node import *


class Body:
    nodes = []
    edges = []

    def __init__(self, entities=None):
        for obj in entities:
            if isinstance(obj, Node):
                self.nodes.append(obj)
            elif isinstance(obj, Edge):
                self.edges.append(obj)

    def add_nodes(self, nodes):
        self.nodes.extend(nodes)

    def add_edges(self, edges):
        self.edges.extend(edges)

    def mat(self, mat):
        for node in self.nodes:
            node.change_mat(mat)
