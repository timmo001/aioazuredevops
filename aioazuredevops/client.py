"""Get data from the Azure DevOps API."""

from datetime import datetime
import re

import aiohttp

from aioazuredevops.builds import DevOpsBuild, DevOpsBuildDefinition, DevOpsBuildLinks
from aioazuredevops.core import DevOpsLinks, DevOpsProject, DevOpsTeam
from aioazuredevops.wiql import DevOpsWiqlColumn, DevOpsWiqlResult, DevOpsWiqlWorkItem
from aioazuredevops.work_item import (
    DevOpsWorkItem,
    DevOpsWorkItemAvatar,
    DevOpsWorkItemLinks,
    DevOpsWorkItemUser,
    DevOpsWorkItemValue,
    DevOpsWorkItemValueFields,
)


def sanitize_project_name(project: str) -> str:
    """Sanitize project name."""
    if not re.match(r"^[\w\s]+$", project):
        raise ValueError("Invalid project name")
    return project


class DevOpsClient:
    """Client for Azure DevOps."""

    def __init__(self) -> None:
        """Initilalize."""
        self._authorized = False
        self._pat = None

    @property
    def authorized(self):
        """Is the client authorized."""
        return self._authorized

    @property
    def pat(self):
        """Get the PAT."""
        return self._pat

    async def get(
        self,
        session: aiohttp.ClientSession,
        url: str,
    ) -> aiohttp.ClientResponse:
        """Run a GET request and return response."""
        if self._pat is None:
            return await session.get(url)
        return await session.get(
            url,
            headers={"Authorization": aiohttp.BasicAuth("", self._pat).encode()},
        )

    async def post(
        self,
        session: aiohttp.ClientSession,
        url: str,
        data: dict,
    ) -> aiohttp.ClientResponse:
        """Run a POST request and return response."""
        if self._pat is None:
            return await session.post(
                url,
                json=data,
            )
        return await session.post(
            url,
            json=data,
            headers={"Authorization": aiohttp.BasicAuth("", self._pat).encode()},
        )

    async def authorize(
        self,
        pat: str,
        organization: str,
    ) -> None:
        """Authorize the client."""
        async with aiohttp.ClientSession() as session:
            self._pat = pat
            response: aiohttp.ClientResponse = await self.get(
                session, f"https://dev.azure.com/{organization}/_apis/projects"
            )
            if response.status == 200:
                self._authorized = True
            else:
                self._authorized = False

    async def get_project(
        self,
        organization: str,
        project: str,
    ) -> DevOpsProject | None:
        """Get Azure DevOps project."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.get(
                session,
                f"https://dev.azure.com/{organization}/_apis/projects/{project}",
            )
            if response.status != 200:
                return None

            if (json := await response.json()) is None:
                return None

            return DevOpsProject(
                json["id"],
                json["name"],
                json.get("description", None),
                json.get("url", None),
                json.get("state", None),
                json.get("revision", None),
                json.get("visibility", None),
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
        self,
        organization: str,
        project: str,
        parameters: str,
    ) -> list[DevOpsBuild] | None:
        """Get Azure DevOps builds."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.get(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/build/builds{parameters}",
            )
            if response.status != 200:
                return None
            if (json := await response.json()) is None:
                return None

            builds = []
            for build in json["value"]:
                builds.append(
                    DevOpsBuild(
                        build["id"],
                        build.get("buildNumber", None),
                        build.get("status", None),
                        build.get("result", None),
                        build.get("sourceBranch", None),
                        build.get("sourceVersion", None),
                        build.get("priority", None),
                        build.get("reason", None),
                        build.get("queueTime", None),
                        build.get("startTime", None),
                        build.get("startTime", None),
                        DevOpsBuildDefinition(
                            build["definition"]["id"],
                            build["definition"]["name"],
                            build["definition"].get("url", None),
                            build["definition"].get("path", None),
                            build["definition"].get("type", None),
                            build["definition"].get("queueStatus", None),
                            build["definition"].get("revision", None),
                        )
                        if "definition" in build
                        else None,
                        DevOpsProject(
                            build["project"]["id"],
                            build["project"]["name"],
                            build["project"].get("description", None),
                            build["project"].get("url", None),
                            build["project"].get("state", None),
                            build["project"].get("revision", None),
                            build["project"].get("visibility", None),
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
        self,
        organization: str,
        project: str,
        build_id: int,
    ) -> DevOpsBuild | None:
        """Get Azure DevOps builds."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.get(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/build/builds/{build_id}",
            )
            if response.status != 200:
                return None
            if (build := await response.json()) is None:
                return None

            return DevOpsBuild(
                build["id"],
                build.get("buildNumber", None),
                build.get("status", None),
                build.get("result", None),
                build.get("sourceBranch", None),
                build.get("sourceVersion", None),
                build.get("priority", None),
                build.get("reason", None),
                build.get("queueTime", None),
                build.get("startTime", None),
                build.get("startTime", None),
                DevOpsBuildDefinition(
                    build["definition"]["id"],
                    build["definition"]["name"],
                    build["definition"].get("url", None),
                    build["definition"].get("path", None),
                    build["definition"].get("type", None),
                    build["definition"].get("queueStatus", None),
                    build["definition"].get("revision", None),
                )
                if "definition" in build
                else None,
                DevOpsProject(
                    build["project"]["id"],
                    build["project"]["name"],
                    build["project"].get("description", None),
                    build["project"].get("url", None),
                    build["project"].get("state", None),
                    build["project"].get("revision", None),
                    build["project"].get("visibility", None),
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

    async def get_work_items_ids_all(
        self,
        organization: str,
        project: str,
    ) -> DevOpsWiqlResult | None:
        """Get Azure DevOps work item ids from wiql."""
        project = sanitize_project_name(project)

        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.post(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0",
                {
                    "query": f"Select [System.Id] From WorkItems Where [System.TeamProject] = '{project}'",  # noqa: S608
                },
            )
            if response.status != 200:
                return None
            if (data := await response.json()) is None:
                return None

            return DevOpsWiqlResult(
                query_type=data["queryType"],
                query_result_type=data["queryResultType"],
                as_of=data["asOf"],
                columns=[
                    DevOpsWiqlColumn(
                        reference_name=column["referenceName"],
                        name=column["name"],
                        url=column["url"],
                    )
                    for column in data["columns"]
                ],
                work_items=[
                    DevOpsWiqlWorkItem(
                        id=work_item["id"],
                        url=work_item["url"],
                    )
                    for work_item in data["workItems"]
                ],
            )

    async def get_work_items(
        self,
        organization: str,
        project: str,
        ids: list[int],
    ) -> DevOpsWorkItem | None:
        """Get Azure DevOps work items."""
        async with aiohttp.ClientSession() as session:
            response: aiohttp.ClientResponse = await self.get(
                session,
                f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems?ids={','.join(str(id) for id in ids)}&api-version=6.0",
            )
            if response.status != 200:
                return None
            if (data := await response.json()) is None:
                return None

            return DevOpsWorkItem(
                count=data["count"],
                value=[
                    DevOpsWorkItemValue(
                        id=work_item["id"],
                        rev=work_item["rev"],
                        fields=DevOpsWorkItemValueFields(
                            area_path=work_item["fields"]["System.AreaPath"],
                            team_project=work_item["fields"]["System.TeamProject"],
                            iteration_path=work_item["fields"]["System.IterationPath"],
                            work_item_type=work_item["fields"]["System.WorkItemType"],
                            state=work_item["fields"]["System.State"],
                            reason=work_item["fields"]["System.Reason"],
                            assigned_to=DevOpsWorkItemUser(
                                display_name=work_item["fields"]["System.AssignedTo"][
                                    "displayName"
                                ],
                                url=work_item["fields"]["System.AssignedTo"]["url"],
                                links=DevOpsWorkItemLinks(
                                    avatar=DevOpsWorkItemAvatar(
                                        href=work_item["fields"]["System.AssignedTo"][
                                            "_links"
                                        ]["avatar"]["href"],
                                    ),
                                ),
                                id=work_item["fields"]["System.AssignedTo"]["id"],
                                unique_name=work_item["fields"]["System.AssignedTo"][
                                    "uniqueName"
                                ],
                                image_url=work_item["fields"]["System.AssignedTo"][
                                    "imageUrl"
                                ],
                                descriptor=work_item["fields"]["System.AssignedTo"][
                                    "descriptor"
                                ],
                            )
                            if "System.AssignedTo" in work_item["fields"]
                            and work_item["fields"]["System.AssignedTo"]
                            else None,
                            created_date=work_item["fields"]["System.CreatedDate"],
                            created_by=DevOpsWorkItemUser(
                                display_name=work_item["fields"]["System.CreatedBy"][
                                    "displayName"
                                ],
                                url=work_item["fields"]["System.CreatedBy"]["url"],
                                links=DevOpsWorkItemLinks(
                                    avatar=DevOpsWorkItemAvatar(
                                        href=work_item["fields"]["System.CreatedBy"][
                                            "_links"
                                        ]["avatar"]["href"],
                                    ),
                                ),
                                id=work_item["fields"]["System.CreatedBy"]["id"],
                                unique_name=work_item["fields"]["System.CreatedBy"][
                                    "uniqueName"
                                ],
                                image_url=work_item["fields"]["System.CreatedBy"][
                                    "imageUrl"
                                ],
                                descriptor=work_item["fields"]["System.CreatedBy"][
                                    "descriptor"
                                ],
                            )
                            if "System.CreatedBy" in work_item["fields"]
                            and work_item["fields"]["System.CreatedBy"]
                            else None,
                            changed_date=work_item["fields"]["System.ChangedDate"],
                            changed_by=DevOpsWorkItemUser(
                                display_name=work_item["fields"]["System.ChangedBy"][
                                    "displayName"
                                ],
                                url=work_item["fields"]["System.ChangedBy"]["url"],
                                links=DevOpsWorkItemLinks(
                                    avatar=DevOpsWorkItemAvatar(
                                        href=work_item["fields"]["System.ChangedBy"][
                                            "_links"
                                        ]["avatar"]["href"],
                                    ),
                                ),
                                id=work_item["fields"]["System.ChangedBy"]["id"],
                                unique_name=work_item["fields"]["System.ChangedBy"][
                                    "uniqueName"
                                ],
                                image_url=work_item["fields"]["System.ChangedBy"][
                                    "imageUrl"
                                ],
                                descriptor=work_item["fields"]["System.ChangedBy"][
                                    "descriptor"
                                ],
                            )
                            if "System.ChangedBy" in work_item["fields"]
                            and work_item["fields"]["System.ChangedBy"]
                            else None,
                            comment_count=work_item["fields"]["System.CommentCount"],
                            title=work_item["fields"]["System.Title"],
                            microsoft_vsts_common_state_change_date=work_item["fields"],
                            microsoft_vsts_common_priority=work_item["fields"][
                                "Microsoft.VSTS.Common.Priority"
                            ],
                        ),
                        url=work_item["url"],
                    )
                    for work_item in data["value"]
                ],
            )
