"""DevOps Core. https://docs.microsoft.com/en-gb/rest/api/azure/devops/core/?view=azure-devops-rest-5.1"""
from datetime import datetime
from typing import List


class DevOpsLinks:
    """Links."""

    def __init__(self, linkSelf: str, linkCollection: str, linkWeb: str):
        """Initialize"""
        self.self = linkSelf
        self.collection = linkCollection
        self.web = linkWeb


class DevOpsTeam:
    """DevOps Team."""

    def __init__(self, id: str, name: str, url: str):
        """Initialize"""
        self.id = id
        self.name = name
        self.url = url


class DevOpsProject:
    """A DevOps Project"""

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        url: str,
        state: str,
        revision: int,
        links: DevOpsLinks,
        visibility: str,
        default_team: DevOpsTeam,
        last_updated: datetime,
    ):
        """Initialize"""
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.state = state
        self.revision = revision
        self.links = links
        self.visibility = visibility
        self.default_team = default_team
        self.last_updated = last_updated
