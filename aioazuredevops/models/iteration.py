"""Azure DevOps iteration model."""

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from . import ListResult


class IterationTimeFrame(StrEnum):
    """Iteration timeframe."""

    CURRENT = "current"
    FUTURE = "future"
    PAST = "past"


@dataclass
class IterationAttributes:
    """Azure DevOps iteration attributes."""

    start_date: datetime
    finish_date: datetime
    time_frame: IterationTimeFrame


@dataclass
class Iteration:
    """Azure DevOps iteration."""

    id: UUID
    name: str
    path: str
    attributes: IterationAttributes
    url: str


type IterationsResult = ListResult[Iteration]
