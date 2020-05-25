"""DevOps Builds. https://docs.microsoft.com/en-gb/rest/api/azure/devops/build/builds?view=azure-devops-rest-5.1"""
from datetime import datetime

from aioazuredevops.core import DevOpsProject


class DevOpsBuildLinks:
    """DevOps build links."""

    def __init__(
        self,
        lSelf: str = None,
        web: str = None,
        source_version_display_uri: str = None,
        timeline: str = None,
        badge: str = None,
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
        url: str = None,
        path: str = None,
        type: str = None,
        queue_status: str = None,
        revision: int = None,
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
        build_number: str = None,
        status: str = None,
        result: str = None,
        source_branch: str = None,
        source_version: str = None,
        priority: str = None,
        reason: str = None,
        queue_time: str = None,
        start_time: str = None,
        finish_time: str = None,
        definition: DevOpsBuildDefinition = None,
        project: DevOpsProject = None,
        links: DevOpsBuildLinks = None,
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
