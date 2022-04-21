from .Body import *
from .Node import *


class World:

    def __init__(self, size=V2D(0.0, 0.0), g=V2D(0.0, 10), steps=8):
        self.nodes = []
        self.edges = []
        self.bodies = []

        self.size = size
        self.mid = 0.5 * size
        self.gravity = g

        if steps <= 1:
            self.steps = 1
            self.delta = 1.0
        else:
            self.steps = steps
            self.delta = 1.0 / self.steps

    def step(self):
        for _ in range(self.steps):
            for node in self.nodes:
                node.add_accel(self.gravity)
                node.step()
                node.apply_bound()
                node.reset()
            for edge in self.edges:
                edge.move()

    def add_node(self, x, y, mat=None):
        node = Node(self, x, y, mat)
        self.nodes.append(node)
        return node

    def add_edge(self, p1: Node, p2: Node, scalar, length=None):
        edge = Edge(p1, p2, scalar, length)
        self.edges.append(edge)
        return edge

    def add_body(self, *params):
        body = Body(params)
        self.bodies.append(body)
        return body
