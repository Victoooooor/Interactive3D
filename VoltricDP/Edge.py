from .Node import *


class Edge:

    def __init__(self, p1: Node, p2: Node, scalar, length=None):
        self.p1 = p1
        self.p2 = p2
        self.scalar = scalar
        if length is None:
            self.free_len = abs(self.p2.curr - self.p1.curr)
        else:
            self.free_len = length

    def move(self):
        displace = self.p2.curr - self.p1.curr
        length = abs(displace)

        if length > 0:
            force = 0.5 * self.scalar * (length - self.free_len) * displace / length

            if self.p1.mass != 0.0 and not self.p2.mass:
                self.p1.apply_impulse(2.0 * force)

            elif not self.p1.mass and self.p2.mass != 0.0:
                self.p2.apply_impulse(2.0 * -force)

            else:
                self.p1.apply_impulse(force)
                self.p2.apply_impulse(-force)
