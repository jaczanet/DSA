class TombstoneType:
    """The type of the Tombstone singleton."""

    # Inspired by the implementation of NoneType.

    __slots__ = ()
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __bool__(self, /):
        return False

    def __repr__(self, /):
        return 'Tombstone'


Tombstone = TombstoneType()
