"""Basic WIQL Query to get all work items in a project.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/wit/wiql/query-by-wiql?view=azure-devops-rest-6.0
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class DevOpsWiqlColumn:
    """Azure DevOps WIQL Column."""

    reference_name: str
    name: str
    url: str


@dataclass
class DevOpsWiqlWorkItem:
    """Azure DevOps WIQL Work Item."""

    id: int
    url: str


@dataclass
class DevOpsWiqlResult:
    """Azure DevOps WIQL Result."""

    query_type: str
    query_result_type: str
    as_of: datetime
    columns: list[DevOpsWiqlColumn]
    work_items: list[DevOpsWiqlWorkItem]
