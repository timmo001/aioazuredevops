"""Basic WIQL Query to get all work items in a project.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-7.2-preview
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class WIQLColumn:
    """Azure DevOps WIQL Column."""

    reference_name: str
    name: str
    url: str


@dataclass
class WIQLWorkItem:
    """Azure DevOps WIQL Work Item."""

    id: int
    url: str


@dataclass
class WIQLResult:
    """Azure DevOps WIQL Result."""

    query_type: str
    query_result_type: str
    as_of: datetime
    columns: list[WIQLColumn]
    work_items: list[WIQLWorkItem]
