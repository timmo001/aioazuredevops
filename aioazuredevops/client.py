"""Get data from the Azure DevOps API."""
import asyncio
import json
import sys
from datetime import datetime, timedelta

import aiohttp

from aioazuredevops import DevOpsLinks, DevOpsProject, DevOpsTeam


class DevOpsClient:
    """Client for Azure DevOps."""

    def __init__(self) -> None:
        """Initilalize."""
        self.pat = None

    async def get_request(self, pat: str, url: str) -> aiohttp.ClientResponse:
        """Runs a GET request and returns response"""
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url,
                headers={"Authorization": aiohttp.BasicAuth("", pat).encode()}
                if pat is not None
                else {},
            )
            response.raise_for_status()
        return response

    async def authorize(self, pat: str, organization: str) -> bool:
        """Authenticate."""
        response = await self.get_request(
            pat, f"https://dev.azure.com/{organization}/_apis/projects"
        )
        if response.status is 200:
            self.pat = pat
            return True
        return False

    async def get_project(self, organization: str, project: str) -> DevOpsProject:
        """Get DevOps project."""
        response = await self.get_request(
            self.pat, f"https://dev.azure.com/{organization}/_apis/projects/{project}"
        )
        if response.status is not 200:
            return None
        json = await response.json()
        if json is None:
            return None

        return DevOpsProject(
            json["id"],
            json["name"],
            json["description"],
            json["url"],
            json["state"],
            json["revision"],
            DevOpsLinks(
                json["_links"]["self"]["href"],
                json["_links"]["collection"]["href"],
                json["_links"]["web"]["href"],
            ),
            json["visibility"],
            DevOpsTeam(
                json["defaultTeam"]["id"],
                json["defaultTeam"]["name"],
                json["defaultTeam"]["url"],
            ),
            datetime.strptime(json["lastUpdateTime"], "%Y-%m-%dT%H:%M:%S.%fZ"),
        )
