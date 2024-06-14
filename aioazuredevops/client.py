"""Get data from the Azure DevOps API."""

from datetime import datetime
from typing import Final

import aiohttp

from aioazuredevops.builds import DevOpsBuild, DevOpsBuildDefinition, DevOpsBuildLinks
from aioazuredevops.core import (
    Capabilities,
    DefaultTeam,
    LinkCollection,
    Links,
    ProcessTemplate,
    Project,
    VersionControl,
)
from aioazuredevops.wiql import WIQLColumn, WIQLResult, WIQLWorkItem
from aioazuredevops.work_item import (
    DevOpsWorkItem,
    DevOpsWorkItemAvatar,
    DevOpsWorkItemFields,
    DevOpsWorkItemLinks,
    DevOpsWorkItems,
    DevOpsWorkItemUser,
)

BASE_URL: Final[str] = "https://dev.azure.com"
API_VERSION: Final[str] = "7.2-preview"


class DevOpsClient:
    """Client for Azure DevOps."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initilalize."""
        self._authorized: bool = False
        self._pat: str | None = None
        self._session: aiohttp.ClientSession = session

    @property
    def authorized(self):
        """Is the client authorized."""
        return self._authorized

    @property
    def pat(self):
        """Get the PAT."""
        return self._pat

    async def _get(
        self,
        url: str,
    ) -> aiohttp.ClientResponse:
        """Run a GET request and return response."""
        if self._pat is None:
            return await self._session.get(url)
        return await self._session.get(
            url,
            headers={
                "Authorization": aiohttp.BasicAuth("", self._pat).encode(),
            },
        )

    async def _post(
        self,
        url: str,
        data: dict,
    ) -> aiohttp.ClientResponse:
        """Run a POST request and return response."""
        if self._pat is None:
            return await self._session.post(
                url,
                json=data,
            )
        return await self._session.post(
            url,
            json=data,
            headers={
                "Authorization": aiohttp.BasicAuth("", self._pat).encode(),
            },
        )

    async def authorize(
        self,
        pat: str,
        organization: str,
    ) -> bool:
        """Authorize the client."""
        self._pat = pat
        response: aiohttp.ClientResponse = await self._get(
            f"{BASE_URL}/{organization}/_apis/projects?api-version={API_VERSION}"
        )
        if response.status == 200:
            self._authorized = True
        else:
            self._authorized = False

        return self._authorized

    async def get_project(
        self,
        organization: str,
        project: str,
    ) -> Project | None:
        """Get Azure DevOps project."""
        response: aiohttp.ClientResponse = await self._get(
            f"{BASE_URL}/{organization}/_apis/projects/{project}?includeCapabilities=true&includeHistory=true&api-version={API_VERSION}"
        )
        if response.status != 200:
            return None
        if (json := await response.json()) is None:
            return None

        return Project(
            id=json["id"],
            name=json["name"],
            description=json["description"],
            url=json["url"],
            state=json["state"],
            capabilities=Capabilities(
                process_template=ProcessTemplate(
                    json["capabilities"]["processTemplate"]["templateName"],
                    json["capabilities"]["processTemplate"]["templateTypeId"],
                ),
                versioncontrol=VersionControl(
                    json["capabilities"]["versioncontrol"]["sourceControlType"],
                    json["capabilities"]["versioncontrol"]["gitEnabled"],
                    json["capabilities"]["versioncontrol"]["tfvcEnabled"],
                ),
            ),
            revision=json["revision"],
            links=Links(
                links_self=LinkCollection(json["_links"]["self"]["href"]),
                collection=LinkCollection(json["_links"]["collection"]["href"]),
                web=LinkCollection(json["_links"]["web"]["href"]),
            ),
            visibility=json["visibility"],
            default_team=DefaultTeam(
                id=json["defaultTeam"]["id"],
                name=json["defaultTeam"]["name"],
                url=json["defaultTeam"]["url"],
            ),
            last_update_time=datetime.strptime(
                json["lastUpdateTime"],
                "%Y-%m-%dT%H:%M:%S.%fZ",
            ),
        )

    async def get_builds(
        self,
        organization: str,
        project: str,
        parameters: str,
    ) -> list[DevOpsBuild] | None:
        """Get Azure DevOps builds."""
        response: aiohttp.ClientResponse = await self._get(
            f"{BASE_URL}/{organization}/{project}/_apis/build/builds{parameters}&api-version={API_VERSION}",
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
                    Project(
                        id=build["project"]["id"],
                        name=build["project"]["name"],
                        description=build["project"].get("description", None),
                        url=build["project"].get("url", None),
                        state=build["project"].get("state", None),
                        revision=build["project"].get("revision", None),
                        visibility=build["project"].get("visibility", None),
                        last_update_time=datetime.strptime(
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
        """Get Azure DevOps build."""
        response: aiohttp.ClientResponse = await self._get(
            f"{BASE_URL}/{organization}/{project}/_apis/build/builds/{build_id}?api-version={API_VERSION}"
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
            Project(
                id=build["project"]["id"],
                name=build["project"]["name"],
                description=build["project"].get("description", None),
                url=build["project"].get("url", None),
                state=build["project"].get("state", None),
                revision=build["project"].get("revision", None),
                visibility=build["project"].get("visibility", None),
                last_update_time=datetime.strptime(
                    build["project"]["lastUpdateTime"],
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                )
                if "lastUpdateTime" in build["project"]
                else None,
            )
            if "project" in build
            else None,
            DevOpsBuildLinks(
                build["_links"]["self"]["href"] if "self" in build["_links"] else None,
                build["_links"]["web"]["href"] if "web" in build["_links"] else None,
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
    ) -> WIQLResult | None:
        """Get Azure DevOps work item ids from wiql."""
        response: aiohttp.ClientResponse = await self._post(
            f"{BASE_URL}/{organization}/{project}/_apis/wit/wiql?api-version={API_VERSION}",
            {
                "query": "SELECT [System.Id] From workitems",
            },
        )
        if response.status != 200:
            return None
        if (data := await response.json()) is None:
            return None

        return WIQLResult(
            query_type=data["queryType"],
            query_result_type=data["queryResultType"],
            as_of=data["asOf"],
            columns=[
                WIQLColumn(
                    reference_name=column["referenceName"],
                    name=column["name"],
                    url=column["url"],
                )
                for column in data["columns"]
            ],
            work_items=[
                WIQLWorkItem(
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
    ) -> DevOpsWorkItems | None:
        """Get Azure DevOps work items."""
        response: aiohttp.ClientResponse = await self._get(
            f"{BASE_URL}/{organization}/{project}/_apis/wit/workitems?ids={','.join(str(id) for id in ids)}&api-version={API_VERSION}"
        )
        if response.status != 200:
            return None
        if (data := await response.json()) is None:
            return None

        return DevOpsWorkItems(
            count=data["count"],
            value=[
                DevOpsWorkItem(
                    id=work_item["id"],
                    rev=work_item["rev"],
                    fields=DevOpsWorkItemFields(
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
