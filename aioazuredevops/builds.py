"""DevOps Builds. https://docs.microsoft.com/en-gb/rest/api/azure/devops/build/builds?view=azure-devops-rest-5.1"""
from datetime import datetime

from aioazuredevops.core import DevOpsProject


class DevOpsBuildLinks:
    """DevOps build links."""

    def __init__(
        self,
        lSelf: str,
        web: str,
        source_version_display_uri: str,
        timeline: str,
        badge: str,
    ):
        """Initialize"""
        self.self = lSelf
        self.web = web
        self.source_version_display_uri = source_version_display_uri
        self.timeline = timeline
        self.badge = badge


class DevOpsBuildDefinition:
    """DevOps build definition."""

    def __init__(
        self,
        id: int,
        name: str,
        url: str,
        path: str,
        type: str,
        queue_status: str,
        revision: int,
    ):
        self.id = id
        self.name = name
        self.url = url
        self.path = path
        self.type = type
        self.queue_status = queue_status
        self.revision = revision


class DevOpsBuild:
    """DevOps build."""

    def __init__(
        self,
        id: int,
        links: DevOpsBuildLinks,
        build_number: str,
        status: str,
        result: str,
        source_branch: str,
        source_version: str,
        priority: str,
        reason: str,
        queue_time: str,
        start_time: str,
        finish_time: str,
        definition: DevOpsBuildDefinition,
        project: DevOpsProject,
    ):
        """Initialize"""
        self.id = id
        self.links = links
        self.build_number = build_number
        self.status = status
        self.result = result
        self.source_branch = source_branch
        self.source_version = source_version
        self.priority = priority
        self.reason = reason
        self.queue_time = queue_time
        self.start_time = start_time
        self.finish_time = finish_time
        self.definition = definition
        self.project = project
