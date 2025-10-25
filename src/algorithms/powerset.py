def powerset(s: 'iterable') -> set[frozenset]:
    """The power set of a set S is the set of all subsets of S, including the empty set and S itself."""
    result = [frozenset()]
    for e in s:
        for i in range(len(result)):
            result.append(result[i] | {e})
    return set(result)
