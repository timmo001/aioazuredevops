"""DevOps Core. https://docs.microsoft.com/en-gb/rest/api/azure/devops/core/?view=azure-devops-rest-5.1"""
from datetime import datetime
from typing import List


class DevOpsLinks:
    """Links."""

    def __init__(
        self, linkSelf: str = None, linkCollection: str = None, linkWeb: str = None
    ):
        """Initialize"""
        self.self = linkSelf
        self.collection = linkCollection
        self.web = linkWeb


class DevOpsTeam:
    """DevOps Team."""

    def __init__(self, id: str, name: str, url: str = None):
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
        description: str = None,
        url: str = None,
        state: str = None,
        revision: int = None,
        visibility: str = None,
        last_updated: datetime = None,
        default_team: DevOpsTeam = None,
        links: DevOpsLinks = None,
    ):
        """Initialize"""
        self.id = id
        self.name = name
        self.description = description
        self.url = url
        self.state = state
        self.revision = revision
        self.visibility = visibility
        self.last_updated = last_updated
        self.default_team = default_team
        self.links = links
