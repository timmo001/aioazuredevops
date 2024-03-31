"""DevOps Core.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/core/?view=azure-devops-rest-6.0
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class DevOpsLinks:
    """Links."""

    l_self: str | None = None
    collection: str | None = None
    web: str | None = None


@dataclass
class DevOpsTeam:
    """DevOps Team."""

    team_id: str
    name: str
    url: str | None = None


@dataclass
class DevOpsProject:
    """A DevOps Project."""

    project_id: str
    name: str
    description: str | None = None
    url: str | None = None
    state: str | None = None
    revision: int | None = None
    visibility: str | None = None
    last_updated: datetime | None = None
    default_team: DevOpsTeam | None = None
    links: DevOpsLinks | None = None
