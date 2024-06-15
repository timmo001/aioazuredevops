"""Models."""

from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass
class ListResult[T]:
    """List result."""

    count: int
    value: list[T]
