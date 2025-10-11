from __future__ import annotations

from copy import copy as shallowcopy
from dataclasses import dataclass
from functools import wraps


# Node


@dataclass(slots=True)
class Node:
    value: object
    next: Node = None


# Linked list


def lexicographicalminimum(method):

    # This is a factory function (see "python closures/decorators")
    # to retain logic shared between __lt__ and __le__.

    # __lt__ and __le__ compare the lists element-wise using the same
    # logic until one is exhausted. If all compared elements are equal
    # the list lengths are compared to determine the final truth value.

    if (methodname := method.__name__) != '__lt__' and methodname != '__le__':
        raise ValueError(f"method '{methodname}' is not '__lt__' or '__le__'")

    lengthscomparator = getattr(int, methodname)

    # A dedicated implementation for __le__ is more efficient than
    # combining __lt__ and __eq__ method calls. In the worst case,
    # T(n) to compute __le__ := (__lt__ or __eq__) would be ~ 2*n.
    # A dedicated implementation keeps T(n) ~ n in the worst case.

    @wraps(method)
    def wrapper(self, other):

        # lexicographical comparison
        for x, y in zip(self, other):
            if x < y:
                return True
            if x > y:
                return False

        # fallback to lengths comparison
        return lengthscomparator(len(self), len(other))

    return wrapper


def _updatelength(diff=0, *, reset=False):
    def decorator(method):

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            if reset:
                self._length = 0
            self._length += diff
            return result

        return wrapper

    return decorator


class linkedlist:
    """
    Singly linked list: mutable sequence.

    If no argument is given, the constructor creates a new empty list.
    The argument must be an iterable if specified.
    """

    __slots__ = ('_head', '_tail', '_length')
    __hash__ = None

    def __init__(self, iterable=(), /):

        # This linked list implementation only implements one sentinel
        # node, the tail. The head will point to a node storing a value.
        # In the case of an empty list the head will point to the tail,
        # the sentinel node.

        self._tail = Node(None)
        self._head = self._tail

        # The sentinel node is not storing any datum for the data
        # structure. It stores a null value and points to a null
        # reference in place of the next-node pointer.

        # This sentinel node is needed for handling edge cases, such as
        # adding elements to an empty list: otherwise head and tail
        # pointers should be initialised when the firt element is added.
        # It is more convenient to define them during initialisation.

        # The sentinel node is not counted in the length of the list,
        # since it is only of useful interest to handle the behavoiur of
        # the data structure, but it is of no interest to the user of
        # such.

        self._length = 0

        # finally build the list
        self.extend(iterable)

    def __iter__(self, /):
        """Implement iter(self)."""
        for node in self._iternodes():
            yield node.value

    def __len__(self, /):
        """Return len(self)."""
        return self._length

    def __getitem__(self, index, /):
        """Return self[index]."""
        return self._getnode(index).value

    def __setitem__(self, index, value, /):
        """Set self[index] to value."""
        self._getnode(index).value = value

    def __delitem__(self, index, /):
        """Delete self[index]."""
        self.pop(index)

    def __repr__(self, /):
        """Return repr(self)."""
        return f"linkedlist(({', '.join(repr(value) for value in self)}))"

    def __str__(self, /):
        """Return str(self)."""
        return ' -> '.join(str(value) for value in self)

    def __eq__(self, other, /):
        """Return self == value."""
        if len(self) == len(other):
            for x, y in zip(self, other):
                if x != y:
                    break
            else:
                return True
        return False

    def __ne__(self, other, /):
        """Return self != value."""
        return not self == other

    @lexicographicalminimum
    def __lt__(self, other, /):
        """Return self < value."""

    @lexicographicalminimum
    def __le__(self, other, /):
        """Return self <= value."""

    def __gt__(self, other, /):
        """Return self > value."""
        return not self <= other

    def __ge__(self, other, /):
        """Return self >= value."""
        return not self < other

    def __add__(self, other, /):
        """Return self + other."""
        newlist = self.copy()
        newlist += other
        return newlist

    def __iadd__(self, other, /):
        """Implement self += other."""
        if not isinstance(other, t := type(self)):
            raise TypeError(f'can only concatenate {t.__name__} (not "{type(other).__name__}") to {t.__name__}')
        self.extend(other)
        return self

    def __mul__(self, number, /):
        """Return self * number."""
        newlist = self.copy()
        newlist *= number
        return newlist

    def __rmul__(self, number, /):
        """Return number * self."""
        return self * number

    def __imul__(self, number, /):
        """Implement self *= number."""
        oglist = self.copy()
        for _ in range(number - 1):
            self += oglist
        return self

    def __reversed__(self, /):
        """Return a reverse iterator over the list."""
        newlist = self.copy()
        newlist.reverse()
        return iter(newlist)

    def insert(self, /, index, value):
        """Insert value before index."""
        try:
            node = self._getnode(index)
        except IndexError:
            # Repoducing behaviour of the built-in python `list`
            if index >= len(self):
                self.append(value)
            else:
                self.insert(0, value)
        else:
            node.next = shallowcopy(node)
            node.value = value
            self._length += 1

    @_updatelength(+1)
    def append(self, value, /):
        """Append value to the end of the list."""
        self._tail.value = value

        # New tail
        self._tail.next = self._tail = Node(None)

    def extend(self, iterable, /):
        """Extend list by appending elements from the iterable."""
        for value in shallowcopy(iterable):
            self.append(value)

    def pop(self, index=-1, /):
        """Remove and return item at index (default last)."""
        node = self._getnode(index)
        oldvalue = node.value
        self._ejectnode(node)
        return oldvalue

    def remove(self, value, /):
        """Remove first occurrence of value."""
        for node in self._iternodes():
            if node.value == value:
                self._ejectnode(node)
                break
        else:
            raise ValueError("linkedlist.remove(x): x not in list")

    @_updatelength(reset=True)
    def clear(self, /):
        """Remove all items from list."""
        self._head = self._tail

    def reverse(self, /):
        """Reverse *IN PLACE*."""

        newtail = prev = Node(None)

        curr = self._head
        while curr is not self._tail:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next

        self._head = prev
        self._tail = newtail

    def swap(self, i, j, /):
        """Swap elements at indices 'i' and 'j' in the list."""

        # More efficient than: self[i], self[j] = self[j], self[i]
        # swaps values with only one pass over the list (instead of four)

        i = self._parseindex(i)
        j = self._parseindex(j)

        node_i = node_j = None
        for index, node in enumerate(self._iternodes()):
            if index == i:
                node_i = node
            if index == j:
                node_j = node
            if node_i and node_j:
                break

        node_i.value, node_j.value = node_j.value, node_i.value

    def isort(self, /, *, key=None, reverse=False):
        """
        Sort the list in ascending order and return None.

        The sort is in-place (i.e. the list itself is modified) and stable (i.e. the
        order of two equal elements is maintained).

        If a key function is given, apply it once to each list item and sort them,
        ascending or descending, according to their function values.

        The reverse flag can be set to sort in descending order.
        """

        if not key:
            key = lambda value: value

        # Due to the nature of insertion sort algorithm, key(value) for
        # each value is computed over and over if not cached.

        # implement memoization
        cache = {}

        def _key(value):
            # use 'id(value)' istead of 'value' itself to support caching of unhashable types
            if (t := id(value)) not in cache:
                cache[t] = key(value)
            return cache[t]

        # Insertion sort algorithm revisited for single linked list:
        # it is only possible to traverse the list in one direction.

        for node_i in self._iternodes():
            for node_j in self._iternodes():
                if node_j is node_i:
                    break
                if _key(node_j.value) > _key(node_i.value):
                    node_i.value, node_j.value = node_j.value, node_i.value

        if reverse:
            self.reverse()

    def index(self, /, value, start=0, stop: int = None):
        """Return first index of value."""
        if stop is None:
            stop = len(self)

        for index, elem in enumerate(self):
            if index < start:
                continue
            if index >= stop:
                break
            if elem == value:
                return index
        else:
            raise ValueError(f"{value!r} is not in list")

    def count(self, value, /):
        """Return number of occurrences of value."""
        count = 0
        for elem in self:
            if elem == value:
                count += 1
        return count

    def copy(self, /):
        """Return a shallow copy of the list."""
        return linkedlist(self)

    def _iternodes(self, /):
        node = self._head
        while node is not self._tail:
            yield node
            node = node.next

    def _parseindex(self, index, /) -> int:
        listlength = len(self)

        # Check type(index)
        if not isinstance(index, int):
            raise TypeError(f"list indices must be integers, not {type(index).__name__}")

        # Parse negative indexing
        if index < 0:
            index += listlength

        # Check index is within bounds
        if not 0 <= index <= listlength - 1:  # if index not in range(listlength)
            raise IndexError('list index out of range')

        return index

    def _getnode(self, index, /) -> Node:
        index = self._parseindex(index)

        for i, node in enumerate(self._iternodes()):
            if i == index:
                return node

    @_updatelength(-1)
    def _ejectnode(self, node: Node, /):
        if (nextnode := node.next) is self._tail:
            self._tail = node

        node.value = nextnode.value
        node.next = nextnode.next
