"""Model for Iteration Work Item."""

from dataclasses import dataclass
from typing import Any


@dataclass
class WorkItemRelationTarget:
    """Work item relation target."""

    id: int
    url: str


@dataclass
class WorkItemRelation:
    """Work item relation."""

    rel: Any
    source: Any
    target: WorkItemRelationTarget


@dataclass
class IterationWorkItemsResult:
    """Iteration work items result."""

    work_item_relations: list[WorkItemRelation]
    url: str
