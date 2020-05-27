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
        self._authorized = False
        self._pat = None

    async def fetch(
        self, session: aiohttp.ClientSession, url: str
    ) -> aiohttp.ClientResponse:
        """Runs a GET request and returns response"""
        if self._pat is None:
            return await session.get(url)
        else:
            return await session.get(
                url,
                headers={"Authorization": aiohttp.BasicAuth("", self._pat).encode()},
            )

    async def authorize(self, pat: str, organization: str) -> None:
        """Authenticate."""
        async with aiohttp.ClientSession() as session:
            self._pat = pat
            response: aiohttp.ClientResponse = await self.fetch(
                session, f"https://dev.azure.com/{organization}/_apis/projects"
            )
            if response.status is 200:
                self._authorized = True
            self._authorized = False

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
                json["description"] if "description" in json else None,
                json["url"] if "url" in json else None,
                json["state"] if "state" in json else None,
                json["revision"] if "revision" in json else None,
                json["visibility"] if "visibility" in json else None,
                datetime.strptime(json["lastUpdateTime"], "%Y-%m-%dT%H:%M:%S.%fZ")
                if "lastUpdateTime" in json
                else None,
                DevOpsTeam(
                    json["defaultTeam"]["id"],
                    json["defaultTeam"]["name"],
                    json["defaultTeam"]["url"],
                )
                if "defaultTeam" in json
                else None,
                DevOpsLinks(
                    json["_links"]["self"]["href"],
                    json["_links"]["collection"]["href"],
                    json["_links"]["web"]["href"],
                )
                if "_links" in json
                else None,
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
                        build["buildNumber"] if "buildNumber" in build else None,
                        build["status"] if "status" in build else None,
                        build["result"] if "result" in build else None,
                        build["sourceBranch"] if "sourceBranch" in build else None,
                        build["sourceVersion"] if "sourceVersion" in build else None,
                        build["priority"] if "priority" in build else None,
                        build["reason"] if "reason" in build else None,
                        build["queueTime"] if "queueTime" in build else None,
                        build["startTime"] if "startTime" in build else None,
                        build["startTime"] if "startTime" in build else None,
                        DevOpsBuildDefinition(
                            build["definition"]["id"],
                            build["definition"]["name"],
                            build["definition"]["url"]
                            if "url" in build["definition"]
                            else None,
                            build["definition"]["path"]
                            if "path" in build["definition"]
                            else None,
                            build["definition"]["type"]
                            if "type" in build["definition"]
                            else None,
                            build["definition"]["queueStatus"]
                            if "queueStatus" in build["definition"]
                            else None,
                            build["definition"]["revision"]
                            if "revision" in build["definition"]
                            else None,
                        )
                        if "definition" in build
                        else None,
                        DevOpsProject(
                            build["project"]["id"],
                            build["project"]["name"],
                            build["project"]["description"]
                            if "description" in build["project"]
                            else None,
                            build["project"]["url"]
                            if "url" in build["project"]
                            else None,
                            build["project"]["state"]
                            if "state" in build["project"]
                            else None,
                            build["project"]["revision"]
                            if "revision" in build["project"]
                            else None,
                            build["project"]["visibility"]
                            if "visibility" in build["project"]
                            else None,
                            datetime.strptime(
                                build["project"]["lastUpdateTime"],
                                "%Y-%m-%dT%H:%M:%S.%fZ",
                            )
                            if "lastUpdateTime" in build["project"]
                            else None,
                        )
                        if "project" in build
                        else None,
                        DevOpsBuildLinks(
                            build["_links"]["self"]["href"]
                            if "self" in build["_links"]
                            else None,
                            build["_links"]["web"]["href"]
                            if "web" in build["_links"]
                            else None,
                            build["_links"]["sourceVersionDisplayUri"]["href"]
                            if "sourceVersionDisplayUri" in build["_links"]
                            else None,
                            build["_links"]["timeline"]["href"]
                            if "timeline" in build["_links"]
                            else None,
                            build["_links"]["badge"]["href"]
                            if "badge" in build["_links"]
                            else None,
                        )
                        if "_links" in build
                        else None,
                    )
                )

            return builds

    async def get_build(
        self, organization: str, project: str, build_id: int
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
                build["buildNumber"] if "buildNumber" in build else None,
                build["status"] if "status" in build else None,
                build["result"] if "result" in build else None,
                build["sourceBranch"] if "sourceBranch" in build else None,
                build["sourceVersion"] if "sourceVersion" in build else None,
                build["priority"] if "priority" in build else None,
                build["reason"] if "reason" in build else None,
                build["queueTime"] if "queueTime" in build else None,
                build["startTime"] if "startTime" in build else None,
                build["startTime"] if "startTime" in build else None,
                DevOpsBuildDefinition(
                    build["definition"]["id"],
                    build["definition"]["name"],
                    build["definition"]["url"]
                    if "url" in build["definition"]
                    else None,
                    build["definition"]["path"]
                    if "path" in build["definition"]
                    else None,
                    build["definition"]["type"]
                    if "type" in build["definition"]
                    else None,
                    build["definition"]["queueStatus"]
                    if "queueStatus" in build["definition"]
                    else None,
                    build["definition"]["revision"]
                    if "revision" in build["definition"]
                    else None,
                )
                if "definition" in build
                else None,
                DevOpsProject(
                    build["project"]["id"],
                    build["project"]["name"],
                    build["project"]["description"]
                    if "description" in build["project"]
                    else None,
                    build["project"]["url"] if "url" in build["project"] else None,
                    build["project"]["state"] if "state" in build["project"] else None,
                    build["project"]["revision"]
                    if "revision" in build["project"]
                    else None,
                    build["project"]["visibility"]
                    if "visibility" in build["project"]
                    else None,
                    datetime.strptime(
                        build["project"]["lastUpdateTime"], "%Y-%m-%dT%H:%M:%S.%fZ",
                    )
                    if "lastUpdateTime" in build["project"]
                    else None,
                )
                if "project" in build
                else None,
                DevOpsBuildLinks(
                    build["_links"]["self"]["href"]
                    if "self" in build["_links"]
                    else None,
                    build["_links"]["web"]["href"]
                    if "web" in build["_links"]
                    else None,
                    build["_links"]["sourceVersionDisplayUri"]["href"]
                    if "sourceVersionDisplayUri" in build["_links"]
                    else None,
                    build["_links"]["timeline"]["href"]
                    if "timeline" in build["_links"]
                    else None,
                    build["_links"]["badge"]["href"]
                    if "badge" in build["_links"]
                    else None,
                )
                if "_links" in build
                else None,
            )

    @property
    def authorized(self):
        return self._authorized

    @property
    def pat(self):
        return self._pat
