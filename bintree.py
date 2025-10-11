from __future__ import annotations

from dataclasses import dataclass


# Node


class _SENTINEL_TYPE:
    # Inspired by the implementation of dataclasses._MISSING_TYPE.
    pass


SENTINEL = _SENTINEL_TYPE()


@dataclass(slots=True, match_args=True)
class Node:
    """Binary Search Tree node implementation."""

    key: object
    left: Node = None
    right: Node = None

    @property
    def _issentinel(self, /) -> bool:
        return self._key is SENTINEL and self.left is None and self.right is None

    def __bool__(self, /):
        return not self._issentinel

    def substitute(self, other, /):
        """Replace self with other *IN PLACE*."""
        for attr in Node.__slots__:
            setattr(self, attr, getattr(other, attr))

    def eject(self, /):
        """Remove self from the binary search tree while preserving BST properties."""

        # 1st case: zero descendants
        # 2nd case: one descendant
        # 3rd case: two descendants

        # Structural pattern matching (PEP 634)
        match self:

            case Node(_, Node(SentinelType()), Node(SentinelType())):
                # turn the (leaf) node into a sentinel node
                self.substitute(Node(SENTINEL))

            case Node(_, descendant, Node(SentinelType())) | Node(_, Node(SentinelType()), descendant):
                # replace the ancestor with its descendant
                self.substitute(descendant)

            case Node(_, left, right):
                # substitute with maximum of the left branch (or minimum of the right branch)
                maxnode = left
                while right := maxnode.right:
                    maxnode = right
                self.key = maxnode.key
                maxnode.eject()


# Binary search tree


class bst:

    __slots__ = ('_root',)
    __hash__ = None

    def __init__(self, rootnode=Node(SENTINEL), /):
        self._root = rootnode

    @property
    def root(self, /) -> Node:
        # Public getter to expose a starting point for traversal methods.
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
            raise ValueError(f'bst.remove({key}): {key} not in tree')

    def search(self, key, /) -> bool:
        """Returns True if key is in self, False otherwise."""
        node = self._binarysearch(key)
        if node:
            return True
        else:
            return False

    def __contains__(self, key):
        return self.search(key)


# Traversals


def preorder(tree: bst, /):
    def _preorder(node):
        if node:
            yield node.key
            yield from _preorder(node.left)
            yield from _preorder(node.right)

    yield from _preorder(tree.root)


def inorder(tree: bst, /):
    def _inorder(node):
        if node:
            yield from _inorder(node.left)
            yield node.key
            yield from _inorder(node.right)

    yield from _inorder(tree.root)


def postorder(tree: bst, /):
    def _postorder(node):
        if node:
            yield from _postorder(node.left)
            yield from _postorder(node.right)
            yield node.key

    yield from _postorder(tree.root)


def breadthfirst(tree: bst, /):
    queue = [tree.root]
    while queue:
        node = queue.pop(0)
        if node:
            yield node.key
            queue.append(node.left)
            queue.append(node.right)


# Preorder and Depth First Search are equivalent in result. But here,
# both are implemented as per their definitions for learning's sake.
def depthfirst(tree: bst, /):
    stack = [tree.root]
    while stack:
        node = stack.pop()
        if node:
            yield node.key
            stack.append(node.right)
            stack.append(node.left)
