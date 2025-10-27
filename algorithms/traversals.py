def breadthfirst(tree, /):
    queue = [tree.root]
    while queue:
        node = queue.pop(0)
        if node:
            yield node.key
            queue.append(node.left)
            queue.append(node.right)


def depthfirst(tree, /):
    stack = [tree.root]
    while stack:
        node = stack.pop()
        if node:
            yield node.key
            stack.append(node.right)
            stack.append(node.left)


# Preorder and Depth-First traversals are equivalent in result. But here,
# both are implemented as per their definitions for learning's sake.


def preorder(tree, /):
    def _preorder(node):
        if node:
            yield node.key
            yield from _preorder(node.left)
            yield from _preorder(node.right)

    yield from _preorder(tree.root)


def inorder(tree, /):
    def _inorder(node):
        if node:
            yield from _inorder(node.left)
            yield node.key
            yield from _inorder(node.right)

    yield from _inorder(tree.root)


def postorder(tree, /):
    def _postorder(node):
        if node:
            yield from _postorder(node.left)
            yield from _postorder(node.right)
            yield node.key

    yield from _postorder(tree.root)


__all__ = [
    'breadthfirst',
    'depthfirst',
    'preorder',
    'inorder',
    'postorder',
]
