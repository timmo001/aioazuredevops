"""DevOps Core.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/core/?view=azure-devops-rest-7.2-preview
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessTemplate:
    """Azure DevOps project process template."""

    template_name: str
    template_type_id: str


@dataclass
class VersionControl:
    """Azure DevOps project version control."""

    source_control_type: str
    git_enabled: str
    tfvc_enabled: str


@dataclass
class Capabilities:
    """Azure DevOps project capabilities."""

    process_template: ProcessTemplate
    versioncontrol: VersionControl


@dataclass
class DefaultTeam:
    """Azure DevOps project default team."""

    id: str
    name: str
    url: str


@dataclass
class LinkCollection:
    """Azure DevOps project collection."""

    href: str


@dataclass
class Links:
    """Azure DevOps project links."""

    links_self: LinkCollection
    collection: LinkCollection
    web: LinkCollection


@dataclass
class Project:
    """Azure DevOps project."""

    id: str
    name: str
    description: str
    url: str
    state: str
    revision: int
    visibility: str
    capabilities: Capabilities | None = None
    links: Links | None = None
    default_team: DefaultTeam | None = None
    last_update_time: datetime | None = None
