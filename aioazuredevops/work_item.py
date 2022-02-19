"""
Work items in a project
https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/work-items/list?view=azure-devops-rest-6.0
"""
from uuid import UUID
from datetime import datetime


class DevOpsWorkItemAvatar:
    href: str

    def __init__(
        self,
        href: str,
    ) -> None:
        self.href = href


class DevOpsWorkItemLinks:
    avatar: DevOpsWorkItemAvatar

    def __init__(
        self,
        avatar: DevOpsWorkItemAvatar,
    ) -> None:
        self.avatar = avatar


class DevOpsWorkItemUser:
    display_name: str
    url: str
    links: DevOpsWorkItemLinks
    id: UUID
    unique_name: None
    image_url: None
    descriptor: str

    def __init__(
        self,
        display_name: str,
        url: str,
        links: DevOpsWorkItemLinks,
        id: UUID,
        unique_name: None,
        image_url: None,
        descriptor: str,
    ) -> None:
        self.display_name = display_name
        self.url = url
        self.links = links
        self.id = id
        self.unique_name = unique_name
        self.image_url = image_url
        self.descriptor = descriptor


class DevOpsWorkItemValueFields:
    area_path: str
    team_project: str
    iteration_path: str
    work_item_type: str
    state: str
    reason: str
    assigned_to: DevOpsWorkItemUser | None
    created_date: datetime
    created_by: DevOpsWorkItemUser
    changed_date: datetime
    changed_by: DevOpsWorkItemUser
    comment_count: int
    title: str
    microsoft_vsts_common_state_change_date: datetime
    microsoft_vsts_common_priority: int

    def __init__(
        self,
        area_path: str,
        team_project: str,
        iteration_path: str,
        work_item_type: str,
        state: str,
        reason: str,
        assigned_to: DevOpsWorkItemUser | None,
        created_date: datetime,
        created_by: DevOpsWorkItemUser,
        changed_date: datetime,
        changed_by: DevOpsWorkItemUser,
        comment_count: int,
        title: str,
        microsoft_vsts_common_state_change_date: datetime,
        microsoft_vsts_common_priority: int,
    ) -> None:
        self.area_path = area_path
        self.team_project = team_project
        self.iteration_path = iteration_path
        self.work_item_type = work_item_type
        self.state = state
        self.reason = reason
        self.assigned_to = assigned_to
        self.created_date = created_date
        self.created_by = created_by
        self.changed_date = changed_date
        self.changed_by = changed_by
        self.comment_count = comment_count
        self.title = title
        self.microsoft_vsts_common_state_change_date = microsoft_vsts_common_state_change_date
        self.microsoft_vsts_common_priority = microsoft_vsts_common_priority


class DevOpsWorkItemValue:
    id: int
    rev: int
    fields: DevOpsWorkItemValueFields
    url: str

    def __init__(
        self,
        id: int,
        rev: int,
        fields: DevOpsWorkItemValueFields,
        url: str,
    ) -> None:
        self.id = id
        self.rev = rev
        self.fields = fields
        self.url = url


class DevOpsWorkItem:
    count: int
    value: list[DevOpsWorkItemValue]

    def __init__(
        self,
        count: int,
        value: list[DevOpsWorkItemValue],
    ) -> None:
        self.count = count
        self.value = value
