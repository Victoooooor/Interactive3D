import math


class V2D:

    def __init__(self, x=0.0, y=0.0):
        self.val = [x, y]

    @property
    def x(self):
        return self.val[0]

    @x.setter
    def x(self, value):
        self.val[0] = value

    @x.deleter
    def x(self):
        del self.val[0]

    @property
    def y(self):
        return self.val[1]

    @y.setter
    def y(self, value):
        self.val[1] = value

    @y.deleter
    def y(self):
        del self.val[1]

    def __abs__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __add__(self, other):
        return V2D(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self.__add__(other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __bool__(self):
        return self.x != 0.0 or self.y != 0.0

    def __copy__(self):
        return self.__class__(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __idiv__(self, other):
        assert type(other) in (int, float)
        self.x /= other
        self.y /= other
        return self

    def __imul__(self, other):
        assert type(other) in (int, float)
        self.x *= other
        self.y *= other
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __iter__(self):
        yield self.x
        yield self.y

    def __mul__(self, other):
        assert type(other) in (int, float)
        return V2D(self.x * other, self.y * other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return V2D(-self.x, -self.y)

    def __pos__(self):
        return V2D(self.x, self.y)

    def __sub__(self, other):
        if other is None:
            return V2D(self.x, self.y)
        return V2D(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        assert type(other) in (int, float)
        return V2D(self.x * other, self.y * other)

    def __str__(self):
        return f'V2D({self.x}, {self.y})'

    def __truediv__(self, other):
        assert type(other) in (int, float)
        return V2D(self.x / other,
                   self.y / other)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def scale(self, other):
        self.x *= other.x
        self.y *= other.y

    @staticmethod
    def zero():
        return V2D(0.0, 0.0)
