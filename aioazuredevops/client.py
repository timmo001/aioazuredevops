"""Get data from the Azure DevOps API."""
import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import List

import aiohttp

from aioazuredevops.core import DevOpsLinks, DevOpsProject, DevOpsTeam
from aioazuredevops.builds import DevOpsBuild, DevOpsBuildDefinition, DevOpsBuildLinks


class DevOpsClient:
    """Client for Azure DevOps."""

    def __init__(self) -> None:
        """Initilalize."""
        self.pat = None

    async def fetch(
        self, session: aiohttp.ClientSession, url: str
    ) -> aiohttp.ClientResponse:
        """Runs a GET request and returns response"""
        if self.pat is None:
            return await session.get(url)
        else:
            return await session.get(
                url, headers={"Authorization": aiohttp.BasicAuth("", self.pat).encode()}
            )

    async def authorize(self, pat: str, organization: str) -> bool:
        """Authenticate."""
        async with aiohttp.ClientSession() as session:
            self.pat = pat
            response: aiohttp.ClientResponse = await self.fetch(
                session, f"https://dev.azure.com/{organization}/_apis/projects"
            )
            if response.status is 200:
                return True
            return False

    async def get_project(self, organization: str, project: str) -> DevOpsProject:
        """Get DevOps project."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.fetch(
                session,
                f"https://dev.azure.com/{organization}/_apis/projects/{project}",
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

    async def get_builds(
        self, organization: str, project: str, parameters: str
    ) -> List[DevOpsBuild]:
        """Get DevOps builds."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.fetch(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/build/builds{parameters}",
            )
            if response.status is not 200:
                return None
            json = await response.json()
            if json is None:
                return None

            builds = []
            for build in json["value"]:
                builds.append(
                    DevOpsBuild(
                        build["id"],
                        DevOpsBuildLinks(
                            build["_links"]["self"]["href"],
                            build["_links"]["web"]["href"],
                            build["_links"]["sourceVersionDisplayUri"]["href"],
                            build["_links"]["timeline"]["href"],
                            build["_links"]["badge"]["href"],
                        ),
                        build["buildNumber"],
                        build["status"],
                        build["result"],
                        build["sourceBranch"],
                        build["sourceVersion"],
                        build["priority"],
                        build["reason"],
                        build["queueTime"],
                        build["startTime"],
                        build["finishTime"],
                        DevOpsBuildDefinition(
                            build["definition"]["id"],
                            build["definition"]["name"],
                            build["definition"]["url"],
                            build["definition"]["path"],
                            build["definition"]["type"],
                            build["definition"]["queueStatus"],
                            build["definition"]["revision"],
                        ),
                    )
                )

            return builds

    async def get_build(
        self, organization: str, project: str, parameters: str, build_id: int
    ) -> DevOpsBuild:
        """Get DevOps builds."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.fetch(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{build_id}",
            )
            if response.status is not 200:
                return None
            build = await response.json()
            if build is None:
                return None

            return DevOpsBuild(
                build["id"],
                DevOpsBuildLinks(
                    build["_links"]["self"]["href"],
                    build["_links"]["web"]["href"],
                    build["_links"]["sourceVersionDisplayUri"]["href"],
                    build["_links"]["timeline"]["href"],
                    build["_links"]["badge"]["href"],
                ),
                build["buildNumber"],
                build["status"],
                build["result"],
                build["sourceBranch"],
                build["sourceVersion"],
                build["priority"],
                build["reason"],
                build["queueTime"],
                build["startTime"],
                build["finishTime"],
                DevOpsBuildDefinition(
                    build["definition"]["id"],
                    build["definition"]["name"],
                    build["definition"]["url"],
                    build["definition"]["path"],
                    build["definition"]["type"],
                    build["definition"]["queueStatus"],
                    build["definition"]["revision"],
                ),
            )
