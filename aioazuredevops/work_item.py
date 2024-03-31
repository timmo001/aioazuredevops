"""Work items in a project.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-6.0
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class DevOpsWorkItemAvatar:
    """Work item avatar."""

    href: str


@dataclass
class DevOpsWorkItemLinks:
    """Work item links."""

    avatar: DevOpsWorkItemAvatar


@dataclass
class DevOpsWorkItemUser:
    """Work item user."""

    display_name: str
    url: str
    links: DevOpsWorkItemLinks
    id: UUID
    unique_name: None
    image_url: None
    descriptor: str


@dataclass
class DevOpsWorkItemValueFields:
    """Azure DevOps work item value fields."""

    area_path: str
    team_project: str
    iteration_path: str
    work_item_type: str
    state: str
    reason: str
    assigned_to: DevOpsWorkItemUser | None
    created_date: datetime
    created_by: DevOpsWorkItemUser | None
    changed_date: datetime
    changed_by: DevOpsWorkItemUser | None
    comment_count: int
    title: str
    microsoft_vsts_common_state_change_date: datetime
    microsoft_vsts_common_priority: int


@dataclass
class DevOpsWorkItemValue:
    """Azure DevOps work item value."""

    id: int
    rev: int
    fields: DevOpsWorkItemValueFields
    url: str


@dataclass
class DevOpsWorkItem:
    """Azure DevOps work item."""

    count: int
    value: list[DevOpsWorkItemValue]
