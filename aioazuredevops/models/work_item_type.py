"""Work item types."""

from dataclasses import dataclass
from enum import StrEnum

from . import ListResult


@dataclass
class Field:
    """Field."""

    always_required: bool
    reference_name: str
    name: str
    url: str
    default_value: str | None = None
    help_text: str | None = None


class Category(StrEnum):
    """Category."""

    COMPLETED = "Completed"
    IN_PROGRESS = "InProgress"
    PROPOSED = "Proposed"
    REMOVED = "Removed"
    RESOLVED = "Resolved"


@dataclass
class State:
    """State."""

    name: str
    color: str
    category: Category


@dataclass
class Transition:
    """Transition."""

    to: str
    actions: list[str] | None = None


@dataclass
class Icon:
    """Icon."""

    id: str
    url: str


@dataclass
class WorkItemType:
    """Work item type."""

    name: str
    reference_name: str
    description: str
    color: str
    icon: Icon
    is_disabled: bool
    xml_form: str
    fields: list[Field]
    field_instances: list[Field]
    transitions: dict[str, list[Transition]]
    states: list[State]
    url: str


type WorkItemTypesResult = ListResult[WorkItemType]
