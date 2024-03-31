"""Test the http client module."""

# from aioresponses import aioresponses
from aioresponses import aioresponses
import pytest

from aioazuredevops.builds import DevOpsBuild
from aioazuredevops.client import BASE_URL, DevOpsClient
from aioazuredevops.core import DevOpsProject
from aioazuredevops.wiql import DevOpsWiqlResult
from aioazuredevops.work_item import (
    DevOpsWorkItem,
    DevOpsWorkItemValue,
    DevOpsWorkItemValueFields,
)

from . import ORGANIZATION, PAT, PROJECT

BAD_PROJECT_NAME = "badproject"
EMPTY_PROJECT_NAME = "emptyproject"


@pytest.mark.asyncio
async def test_authorize(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the authorize method."""
    assert not devops_client.authorized
    assert devops_client.pat is None

    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    assert devops_client.authorized
    assert devops_client.pat == PAT

    # Test with unauthorized (GET with PAT)
    mock_aioresponse.clear()
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/_apis/projects",
        status=401,
    )

    assert not await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    assert not devops_client.authorized
    assert devops_client.pat == PAT


@pytest.mark.asyncio
async def test_get_project(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the get_project method."""
    project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert isinstance(project, DevOpsProject)
    assert project.project_id == "testid"

    # Test with authorization (GET with PAT)
    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    # Test with client error
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/_apis/projects/{BAD_PROJECT_NAME}",
        status=400,
    )

    bad_project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
    )

    assert bad_project is None

    # Test with empty response
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/_apis/projects/{EMPTY_PROJECT_NAME}",
        payload=None,
        status=200,
    )

    empty_project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
    )

    assert empty_project is None


@pytest.mark.asyncio
async def test_get_builds(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the get_builds method."""
    builds = await devops_client.get_builds(
        organization=ORGANIZATION,
        project=PROJECT,
        parameters="",
    )

    assert isinstance(builds, list)
    assert len(builds) == 1
    assert isinstance(builds[0], DevOpsBuild)

    # Test with bad request
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/build/builds",
        status=400,
    )

    bad_builds = await devops_client.get_builds(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
        parameters="",
    )

    assert bad_builds is None

    # Test with empty response
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/build/builds",
        payload=None,
        status=200,
    )

    empty_builds = await devops_client.get_builds(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
        parameters="",
    )

    assert empty_builds is None


@pytest.mark.asyncio
async def test_get_build(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the get_build method."""
    build = await devops_client.get_build(
        organization=ORGANIZATION,
        project=PROJECT,
        build_id=1,
    )

    assert isinstance(build, DevOpsBuild)

    # Test with bad request
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/build/builds/1",
        status=400,
    )

    bad_build = await devops_client.get_build(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
        build_id=1,
    )

    assert bad_build is None

    # Test with empty response
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/build/builds/1",
        payload=None,
        status=200,
    )

    empty_build = await devops_client.get_build(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
        build_id=1,
    )

    assert empty_build is None


@pytest.mark.asyncio
async def test_get_work_items_ids_all(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the get_work_items_ids method."""
    work_items_ids = await devops_client.get_work_items_ids_all(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert isinstance(work_items_ids, DevOpsWiqlResult)

    # Test with authorization (POST with PAT)
    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    work_items_ids = await devops_client.get_work_items_ids_all(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert isinstance(work_items_ids, DevOpsWiqlResult)

    # Test with client error
    mock_aioresponse.post(
        f"{BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/wit/wiql?api-version=6.0",
        status=400,
    )

    bad_work_items_ids = await devops_client.get_work_items_ids_all(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
    )

    assert bad_work_items_ids is None

    # Test with empty response
    mock_aioresponse.post(
        f"{BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/wit/wiql?api-version=6.0",
        payload=None,
        status=200,
    )

    empty_work_items_ids = await devops_client.get_work_items_ids_all(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
    )

    assert empty_work_items_ids is None


@pytest.mark.asyncio
async def test_get_work_items(
    mock_aioresponse: aioresponses,
    devops_client: DevOpsClient,
) -> None:
    """Test the get_work_items method."""
    work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=PROJECT,
        ids=[1],
    )

    assert isinstance(work_items, DevOpsWorkItem)
    assert work_items.count == 1
    assert len(work_items.value) == 1
    assert isinstance(work_items.value[0], DevOpsWorkItemValue)
    assert isinstance(work_items.value[0].fields, DevOpsWorkItemValueFields)

    # Test bad request
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/wit/workitems?ids=1&api-version=6.0",
        status=400,
    )

    bad_work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
        ids=[1],
    )

    assert bad_work_items is None

    # Test with empty response
    mock_aioresponse.get(
        f"{BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/wit/workitems?ids=1&api-version=6.0",
        payload=None,
        status=200,
    )

    empty_work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
        ids=[1],
    )

    assert empty_work_items is None
