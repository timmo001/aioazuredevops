"""DevOps Builds.

https://docs.microsoft.com/en-gb/rest/api/azure/devops/build/builds?view=azure-devops-rest-6.0
"""

from dataclasses import dataclass

from .core import DevOpsProject


@dataclass
class DevOpsBuildLinks:
    """DevOps build links."""

    l_self: str | None = None
    web: str | None = None
    source_version_display_uri: str | None = None
    timeline: str | None = None
    badge: str | None = None


@dataclass
class DevOpsBuildDefinition:
    """DevOps build definition."""

    build_id: int
    name: str
    url: str | None = None
    path: str | None = None
    build_type: str | None = None
    queue_status: str | None = None
    revision: int | None = None


@dataclass
class DevOpsBuild:
    """DevOps build."""

    build_id: int
    build_number: str | None = None
    status: str | None = None
    result: str | None = None
    source_branch: str | None = None
    source_version: str | None = None
    priority: str | None = None
    reason: str | None = None
    queue_time: str | None = None
    start_time: str | None = None
    finish_time: str | None = None
    definition: DevOpsBuildDefinition | None = None
    project: DevOpsProject | None = None
    links: DevOpsBuildLinks | None = None
