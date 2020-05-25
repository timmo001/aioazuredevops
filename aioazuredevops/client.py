"""Get data from the Azure DevOps API."""
import asyncio
import json
import sys
from datetime import datetime, timedelta
from typing import List

import aiohttp

from aioazuredevops.core import DevOpsLinks, DevOpsProject, DevOpsTeam
from aioazuredevops.builds import DevOpsBuild, DevOpsBuildLinks


class DevOpsClient:
    """Client for Azure DevOps."""

    def __init__(self) -> None:
        """Initilalize."""
        self.pat = None

    # async def get_request(self, url: str) -> aiohttp.ClientResponse:
    #     """Runs a GET request and returns response"""
    #     print(url)
    #     async with aiohttp.ClientSession() as session:
    #         response: aiohttp.ClientResponse = await session.get(
    #             url,
    #             headers={"Authorization": aiohttp.BasicAuth("", self.pat).encode()}
    #             if self.pat is not None
    #             else {},
    #         )
    #         return response

    async def authorize(self, pat: str, organization: str) -> bool:
        """Authenticate."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await session.get(
                f"https://dev.azure.com/{organization}/_apis/projects",
                headers={"Authorization": aiohttp.BasicAuth("", self.pat).encode()}
                if self.pat is not None
                else {},
            )
        if response.status is 200:
            self.pat = pat
            return True
        return False
        # response: aiohttp.ClientResponse = await self.get_request(
        #     pat,
        # )

    async def get_project(self, organization: str, project: str) -> DevOpsProject:
        """Get DevOps project."""
        # response: aiohttp.ClientResponse = await self.get_request(
        #     f"https://dev.azure.com/{organization}/_apis/projects/{project}"
        # )
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await session.get(
                f"https://dev.azure.com/{organization}/_apis/projects/{project}",
                headers={"Authorization": aiohttp.BasicAuth("", self.pat).encode()}
                if self.pat is not None
                else {},
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
            response: aiohttp.ClientResponse = await session.get(
                f"https://dev.azure.com/{organization}/{project}/_apis/build/builds{parameters}",
                headers={"Authorization": aiohttp.BasicAuth("", self.pat).encode()}
                if self.pat is not None
                else {},
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
                    )
                )

            return builds
