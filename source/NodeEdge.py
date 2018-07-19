
from array import array
import reprlib
import math
import numbers

class Node:

    coord_names = 'xy'

    def __init__(self, components):
        self._components = array('d', components)


    def __iter__(self):
        return iter(self._components)


    def __repr__(self):
        cls = type(self)
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return '{.__name__}({})'.format(cls, components)


    def __str__(self):
        return str(tuple(self))


    def __eq__(self, other):
        return len(self) == len(other) and all(a == b for a,b in zip(self, other))


    def __abs__(self):
        return math.sqrt(sum(x * x for x in self))


    def __len__(self):
        return len(self._components)


    def __bool__(self):
        return bool(abs(self))


    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{.__name__} indices must be integers'
            raise TypeError(msg.format(cls))


    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:
            pos = cls.coord_names.find(name)
            if 0 <= pos < len(self._components):
                return self._components[pos]

        msg = '{.__name__} has no attribute {}'
        raise AttributeError(msg.format(cls, name))


    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            pos = cls.coord_names.find(name)
            if 0 <= pos < len(self._components):
                self._components[pos] = value
            else:
                msg = 'Attribute name {} not allowed for class {.__name__}'
                raise AttributeError(msg.format(name, cls))
        else:
            super().__setattr__(name, value)


class NodeTautologyError(Exception):
    """Two nodes is the same.
    """
    def __init__(self, message):
        self.message = message


class Edge:

    def __init__(self, v1, v2, direction=False):
        if v1 == v2:
            raise NodeTautologyError('Can\'t edge same Node')
        self.v1 = v1
        self.v2 = v2
        self.direction = bool(direction)


    def __repr__(self):
        cls = type(self)
        direction = ''
        if self.direction:
            direction = ', direction=True'
        return '{.__name__}({}, {}{})'.format(cls, repr(self._v1), repr(self._v2), direction)

    @property
    def v1(self):
        return self._v1


    @v1.setter
    def v1(self, value):
        cls = type(self)
        if isinstance(value, Node):
            self._v1 = value
        else:
            msg = '{.__name__}() argument must be Node'
            raise TypeError(msg.format(cls))


    @property
    def v2(self):
        return self._v2


    @v2.setter
    def v2(self, value):
        cls = type(self)
        if isinstance(value, Node):
            self._v2 = value
        else:
            msg = '{.__name__}() argument must be Node'
            raise TypeError(msg.format(cls))


    def __eq__(self, other):
        return ((self.v1 == other.v1) and (self.v2 == other.v2) and (self.direction == other.direction))


    def __abs__(self):
        s = sum((i - j)**2 for i, j in zip(self.v1, self.v2))
        return math.sqrt(s)

