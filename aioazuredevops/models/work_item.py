"""Work items in a project.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-7.2-preview
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from . import ListResult


@dataclass
class WorkItemAvatar:
    """Work item avatar."""

    href: str


@dataclass
class WorkItemLinks:
    """Work item links."""

    avatar: WorkItemAvatar


@dataclass
class WorkItemUser:
    """Work item user."""

    display_name: str
    url: str
    id: UUID
    unique_name: Any
    image_url: Any
    descriptor: str
    links: WorkItemLinks | None = None


@dataclass
class WorkItemFields:
    """Azure DevOps work item fields."""

    area_path: str
    team_project: str
    iteration_path: str
    work_item_type: str
    state: str
    reason: str
    assigned_to: WorkItemUser | None
    created_date: datetime
    created_by: WorkItemUser | None
    changed_date: datetime
    changed_by: WorkItemUser | None
    comment_count: int
    title: str
    microsoft_vsts_common_state_change_date: datetime
    microsoft_vsts_common_priority: int


@dataclass
class WorkItem:
    """Azure DevOps work item."""

    id: int
    rev: int
    fields: WorkItemFields
    url: str


type WorkItemsResult = ListResult[WorkItem]
