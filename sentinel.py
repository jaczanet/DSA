class _SENTINEL_TYPE:
    def __repr__(self, /):
        return 'SENTINEL'


SENTINEL = _SENTINEL_TYPE()
