from dataclasses import dataclass

from .sentinel import SENTINEL


# Node
@dataclass(slots=True, match_args=True)
class Node:
    """Binary-Search-Tree node implementation."""

    key: object
    left: 'Node' = None
    right: 'Node' = None

    @property
    def _issentinel(self, /) -> bool:
        return self.key is SENTINEL

    def __bool__(self, /):
        """Return bool(self)."""
        return not self._issentinel

    def substitute(self, other, /):
        """Replace self with other *IN PLACE*."""
        for attr in Node.__slots__:
            setattr(self, attr, getattr(other, attr))

    def eject(self, /):
        """Remove self from the binary search tree while preserving BST properties."""
        left = self.left
        right = self.right

        # 1st case: two descendants
        if left and right:
            # substitute with maximum of the left branch (or minimum of the right branch)
            maxnode = left
            while right := maxnode.right:
                maxnode = right
            self.key = maxnode.key
            maxnode.eject()

        # 2nd case: one descendant
        elif (descendant := left) or (descendant := right):  # leveraging short-circuiting
            # replace the ancestor with its descendant
            self.substitute(descendant)

        # 3rd case: zero descendants
        else:
            # turn the (leaf) node into a sentinel node
            self.substitute(Node(SENTINEL))


# Binary Search Tree
class BinarySearchTree:
    """Binary Search Tree implementation."""

    __slots__ = ('_root',)
    __hash__ = None

    def __init__(self, /):
        self._root = Node(SENTINEL)

    @property
    def root(self, /) -> Node:
        # Public getter exposing an entry point for traversal methods.
        return self._root

    def _binarysearch(self, key, /) -> Node:
        """
        Performs a binary search over the binary search tree.

        If found, returns the node containing the key; otherwise,
        returns the sentinel node where the search culminated.
        """

        node = self._root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            elif key == node.key:
                return node
        else:
            return node

    def insert(self, key, /):
        """Insert key in self."""
        node = self._binarysearch(key)
        if node:
            pass  # skip duplicates
        else:
            node.key = key

            # In this implementation of a Binary Search Tree, the leaf
            # nodes' 'left' and 'right' pointers descendants are sentinel
            # nodes in order to reduce edge cases.

            node.left = Node(SENTINEL)
            node.right = Node(SENTINEL)

    def remove(self, key, /):
        """Remove key from self."""
        node = self._binarysearch(key)
        if node:
            node.eject()
        else:
            raise ValueError(f'{type(self).__name__}.remove({key}): {key} not in tree')

    def search(self, key, /) -> bool:
        """Returns True if key is in self, False otherwise."""
        node = self._binarysearch(key)
        if node:
            return True
        else:
            return False

    def __contains__(self, key, /):
        """Return bool(key in self)."""
        return self.search(key)


if __name__ == '__main__':

    keys = (9, 4, 10, 3, 6, 11, 2, 5, 7)

    tree = BinarySearchTree()

    for key in keys:
        tree.insert(key)

    from algorithms.traversals import *

    print(*breadthfirst(tree), ': breadthfirst')
    print(*depthfirst(tree), ': depthfirst')
    print(*preorder(tree), ': preorder')
    print(*inorder(tree), ': inorder')
    print(*postorder(tree), ': postorder')

    print(f'{1 in tree=}')
    print(f'{10 in tree=}')

    tree.remove(10)
    print(f'{10 in tree=}')
