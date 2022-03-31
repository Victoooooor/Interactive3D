import math
import operator


class Vector:
    x = 0.0
    y = 0.0

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)
    length = magnitude = __abs__

    def normalize(self):
        l = self.magnitude()
        if l:
            self.x = self.x / l
            self.y = self.y / l

    def normalized(self):
        l = self.magnitude()
        if l:
            return Vector(self.x / l, self.y / l)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def zero(self):
        self.x = 0.0
        self.y = 0.0

    def one(self):
        self.x = 1.0
        self.y = 1.0

    def tuple(self):
        return (self.x, self.y)

    def scale(self, other):
        self.x *= other.x
        self.y *= other.y

    def to_tuple(self):
        return self.x, self.y

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __nonzero__(self):
        return self.x != 0.0 or self.y != 0.0

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    __radd__ = __add__

    def __iadd_(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        if other is None:
            return Vector(self.x, self.y)
        return Vector(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        assert type(other) in (int, float)
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, other):
        assert type(other) in (int, float)
        return Vector(self.x * other, self.y * other)

    def __imul__(self, other):
        assert type(other) in (int, float)
        self.x *= other
        self.y *= other
        return self

    def __truediv__(self, other):
        assert type(other) in (int, float)
        return Vector(operator.truediv(self.x, other),
                      operator.truediv(self.y, other))

    def __idiv__(self, other):
        assert type(other) in (int, float)
        operator.truediv(self.x, other)
        operator.truediv(self.y, other)
        return self
  #
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __pos__(self):
        return Vector(self.x, self.y)

    def __str__(self):
        return "Vector("+str(self.x)+", "+str(self.y)+")"

    @staticmethod
    def zero():
        return Vector(0.0, 0.0)
