from __future__ import annotations


from functools import wraps, total_ordering
from copy import copy as shallowcopy

from node import Node


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


@total_ordering
class linkedlist:
    """Singly linked list (mutable sequence)."""

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

    def __str__(self, /) -> str:
        return ' -> '.join(str(value) for value in self)

    ## Iterable

    def __iter__(self, /):
        for node in self._iternodes():
            yield node.value

    def _iternodes(self, /):
        node = self._head
        while node is not self._tail:
            yield node
            node = node.next

    ## Sequence

    def __len__(self, /) -> int:
        return self._length

    def __getitem__(self, index: int, /) -> int:
        return self._getnode(index).value

    def _getnode(self, index: int, /) -> Node:
        index = self._parseindex(index)

        for i, node in enumerate(self._iternodes()):
            if i == index:
                return node

    def index(self, /, value, start: int = 0, stop: int = None) -> int:
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

    def count(self, value, /) -> int:
        count = 0
        for elem in self:
            if elem == value:
                count += 1
        return count

    def copy(self, /) -> 'linkedlist':
        # shallow copy
        return linkedlist(self)

    def __reversed__(self, /) -> 'linkedlist':
        newlist = self.copy()
        newlist.reverse()
        return newlist

    ## Mutable

    # adding elements

    @_updatelength(+1)
    def append(self, value, /) -> None:
        self._tail.value = value

        # New tail
        self._tail.next = self._tail = Node(None)

    @_updatelength(diff=0)  # diff=0 because is calling self.append(value)
    def extend(self, iterable, /) -> None:
        for value in iterable:
            self.append(value)

    # @_updatelength(+1) not possible to use due to recursive calls
    def insert(self, index: int, value, /) -> None:
        try:
            node = self._getnode(index)
        except IndexError:
            # repoducing python built-in `list` behaviour
            if index >= len(self):
                self.append(value)
            else:
                self.insert(0, value)
        else:
            node.next = shallowcopy(node)
            node.value = value
            self._length += 1

    # subtracting elements

    @_updatelength(-1)
    def __delnode(self, node: Node, /) -> None:
        if (nextnode := node.next) is self._tail:
            self._tail = node

        node.value = nextnode.value
        node.next = nextnode.next

    @_updatelength(diff=0)  # diff=0 because is calling self.__delnode(node)
    def pop(self, index: int = -1, /) -> 'value':
        node = self._getnode(index)
        oldvalue = node.value
        self.__delnode(node)
        return oldvalue

    @_updatelength(diff=0)  # diff=0 because is calling self.__delnode(node)
    def remove(self, value, /) -> None:
        for node in self._iternodes():
            if node.value == value:
                self.__delnode(node)
                break
        else:
            raise ValueError("linkedlist.remove(x): x not in list")

    @_updatelength(reset=True)
    def clear(self, /) -> None:
        self._head = self._tail

    # updating in place: i.e. preserving len(self)

    def __setitem__(self, index: int, value, /) -> None:
        self._getnode(index).value = value

    def reverse(self, /) -> None:
        newtail = prev = Node(None)

        curr = self._head
        while curr is not self._tail:
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next

        self._head = prev
        self._tail = newtail

    def swap(self, i: int, j: int, /) -> None:
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

    def isort(self, /):
        # insertion sort revisited for single linked list:
        # it is only possible to traverse the list in one direction

        for node_i in self._iternodes():
            for node_j in self._iternodes():
                if node_j is node_i:
                    break
                if node_j.value > node_i.value:
                    node_i.value, node_j.value = node_j.value, node_i.value

    ## Comparison operator methods

    def __eq__(self, other):
        """Return self==value."""

        if len(self) == len(other):
            for x, y in zip(self, other):
                if x != y:
                    break
            else:
                return True

        return False

    def __ne__(self, other):
        """Return self!=value."""
        return not self == other

    def __lt__(self, other):
        """Return self<value."""

        for x, y in zip(self, other):
            if x < y:
                return True
            if x > y:
                return False

        return len(self) < len(other)

    def __le__(self, other):
        """Return self<=value."""

        for x, y in zip(self, other):
            if x < y:
                return True
            if x > y:
                return False

        return len(self) <= len(other)

    def __gt__(self, other):
        """Return self>value."""
        return not self <= other

    def __ge__(self, other):
        """Return self>=value."""
        return not self < other

    # Auxiliary methods

    def _parseindex(self, index: int) -> int:
        listlength = len(self)

        if not isinstance(index, int):
            raise TypeError(
                f"list indices must be integers, not {type(index).__name__}"
            )

        # Parse reverse (negative) indexing
        if index < 0:
            index += listlength

        # Check index is within bounds
        if not 0 <= index <= listlength - 1:
            raise IndexError('list index out of range')

        return index
