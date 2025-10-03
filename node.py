from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Node:
    value: object
    next: Node = None
