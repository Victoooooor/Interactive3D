import math

from .V2D import *


class Node:

    def __init__(self, world, x=0.0, y=0.0, material: tuple = (1.0, 0.8, 0.2)):  # Material: Mass Friction Bounce
        self.world = world
        self.curr = V2D(x, y)
        self.prev = V2D(x, y)
        if material is None:
            self.material = (1.0, 0.8, 0.2)
        else:
            self.material = material
        self.v = V2D(0.0, 0.0)
        self.a = V2D(0.0, 0.0)

    @property
    def mass(self):
        return self.material[0]

    @mass.setter
    def mass(self, value):
        self.material[0] = value

    @mass.deleter
    def mass(self):
        del self.material[0]

    @property
    def friction(self):
        return self.material[1]

    @friction.setter
    def friction(self, value):
        self.material[1] = value

    @friction.deleter
    def friction(self):
        del self.material[1]

    @property
    def bounce(self):
        return self.material[2]

    @bounce.setter
    def bounce(self, value):
        self.material[2] = value

    @bounce.deleter
    def bounce(self):
        del self.material[2]

    def change_mat(self, new_mat: tuple):
        self.material = new_mat

    def step(self):
        if not self.mass:
            return
        self.v = 2.0 * self.curr - self.prev
        self.prev = self.curr
        self.curr = self.v + self.a * self.world.delta ** 2.0
        self.v = self.curr - self.prev
        self.a = V2D.zero()

    def add_accel(self, rate):
        self.a += rate

    def add_force(self, force: V2D):
        if self.mass != 0.0:
            self.a += force / self.mass

    def apply_impulse(self, impulse):
        if self.mass != 0.0:
            self.curr += impulse / self.mass

    def apply_bound(self):
        # edge
        for i in range(2):
            distance = self.curr - self.prev
            com = False
            if self.curr.val[i] < 0.0:
                self.curr.val[i] = -self.curr.val[i]
                com = True
            elif self.curr.val[i] > self.world.size.val[i]:
                self.curr.val[i] = 2.0 * self.world.size.val[i] - self.curr.val[i]
                com = True

            if com:
                self.prev.val[i] = self.curr.val[i] + self.bounce * distance.val[1-i]
                j = distance.val[1-i]
                k = distance.val[i] * self.friction
                t = j
                if j != 0.0:
                    t /= abs(j)
                if abs(j) <= abs(k):
                    if j * t > 0.0:
                        self.curr.val[1-i] -= 2.0 * j
                else:
                    if k * t > 0.0:
                        self.curr.val[1-i] -= k

    def reset(self):
        self.a = V2D.zero()
