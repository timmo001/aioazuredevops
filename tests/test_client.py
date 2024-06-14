"""Test the http client module."""

from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aioazuredevops.client import DEFAULT_API_VERSION, DEFAULT_BASE_URL, DevOpsClient

from . import ORGANIZATION, PAT, PROJECT

BAD_PROJECT_NAME = "badproject"
EMPTY_PROJECT_NAME = "emptyproject"


@pytest.mark.asyncio
async def test_authorize(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
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
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis/projects?api-version={DEFAULT_API_VERSION}",
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
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_project method."""
    project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert project == snapshot(
        name="project",
    )

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
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis/projects/{BAD_PROJECT_NAME}?api-version={DEFAULT_API_VERSION}&includeCapabilities=true&includeHistory=true",
        status=400,
    )

    bad_project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
    )

    assert bad_project is None

    # Test with empty response
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis/projects/{EMPTY_PROJECT_NAME}?api-version={DEFAULT_API_VERSION}&includeCapabilities=true&includeHistory=true",
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
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_builds method."""
    builds = await devops_client.get_builds(
        organization=ORGANIZATION,
        project=PROJECT,
        parameters="",
    )

    assert builds == snapshot(
        name="builds",
    )

    # Test with bad request
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/build/builds?api-version={DEFAULT_API_VERSION}",
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
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/build/builds?api-version={DEFAULT_API_VERSION}",
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
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_build method."""
    build = await devops_client.get_build(
        organization=ORGANIZATION,
        project=PROJECT,
        build_id=1,
    )

    assert build == snapshot(
        name="build",
    )

    # Test with bad request
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/build/builds/1?api-version={DEFAULT_API_VERSION}",
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
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/build/builds/1?api-version={DEFAULT_API_VERSION}",
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
async def test_get_work_items_ids(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_work_items_ids method."""
    work_items_ids = await devops_client.get_work_item_ids(
        organization=ORGANIZATION,
        project=PROJECT,
        max_results=1,
    )

    assert work_items_ids == snapshot(
        name="work_items_ids",
    )

    # Test with authorization (POST with PAT)
    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    work_items_ids = await devops_client.get_work_item_ids(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert work_items_ids == snapshot(
        name="work_items_ids_authorized",
    )

    # Test with client error
    mock_aioresponse.post(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/wit/wiql?api-version={DEFAULT_API_VERSION}",
        status=400,
    )

    bad_work_items_ids = await devops_client.get_work_item_ids(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
    )

    assert bad_work_items_ids is None

    # Test with empty response
    mock_aioresponse.post(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/wit/wiql?api-version={DEFAULT_API_VERSION}",
        payload=None,
        status=200,
    )

    empty_work_items_ids = await devops_client.get_work_item_ids(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
    )

    assert empty_work_items_ids is None


@pytest.mark.asyncio
async def test_get_work_items(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_work_items method."""
    work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=PROJECT,
        ids=[1] * 300,
    )

    assert work_items == snapshot(
        name="work_items",
    )

    # Test bad request
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/wit/workitems?api-version={DEFAULT_API_VERSION}&errorPolicy=omit&ids=1",
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
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/wit/workitems?api-version={DEFAULT_API_VERSION}&errorPolicy=omit&ids=1",
        payload=None,
        status=200,
    )

    empty_work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
        ids=[1],
    )

    assert empty_work_items is None


@pytest.mark.asyncio
async def test_get_work_item_types(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_work_item_types method."""
    work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert work_item_types == snapshot(
        name="work_item_types",
    )

    # Test with authorization (GET with PAT)
    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert work_item_types == snapshot(
        name="work_item_types_authorized",
    )

    # Test with client error
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{BAD_PROJECT_NAME}/_apis/wit/workitemtypes?api-version={DEFAULT_API_VERSION}",
        status=400,
    )

    bad_work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=BAD_PROJECT_NAME,
    )

    assert bad_work_item_types is None

    # Test with empty response
    mock_aioresponse.get(
        f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{EMPTY_PROJECT_NAME}/_apis/wit/workitemtypes?api-version={DEFAULT_API_VERSION}",
        payload=None,
        status=200,
    )

    empty_work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=EMPTY_PROJECT_NAME,
    )

    assert empty_work_item_types is None
