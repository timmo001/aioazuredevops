"""Test the http client module."""

# from aioresponses import aioresponses
import pytest

from aioazuredevops.builds import DevOpsBuild
from aioazuredevops.client import DevOpsClient
from aioazuredevops.core import DevOpsProject
from aioazuredevops.wiql import DevOpsWiqlResult
from aioazuredevops.work_item import (
    DevOpsWorkItem,
    DevOpsWorkItemValue,
    DevOpsWorkItemValueFields,
)

from . import ORGANIZATION, PAT, PROJECT


@pytest.mark.asyncio
async def test_authorize(devops_client: DevOpsClient) -> None:
    """Test the authorize method."""
    assert not devops_client.authorized
    assert devops_client.pat is None

    assert await devops_client.authorize(
        pat=PAT,
        organization=ORGANIZATION,
    )

    assert devops_client.authorized
    assert devops_client.pat == PAT


@pytest.mark.asyncio
async def test_get_project(devops_client: DevOpsClient) -> None:
    """Test the get_project method."""
    project = await devops_client.get_project(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert isinstance(project, DevOpsProject)


@pytest.mark.asyncio
async def test_get_builds(devops_client: DevOpsClient) -> None:
    """Test the get_builds method."""
    builds = await devops_client.get_builds(
        organization=ORGANIZATION,
        project=PROJECT,
        parameters="",
    )

    assert isinstance(builds, list)
    assert len(builds) == 1
    assert isinstance(builds[0], DevOpsBuild)


@pytest.mark.asyncio
async def test_get_build(devops_client: DevOpsClient) -> None:
    """Test the get_build method."""
    build = await devops_client.get_build(
        organization=ORGANIZATION,
        project=PROJECT,
        build_id=1,
    )

    assert isinstance(build, DevOpsBuild)


@pytest.mark.asyncio
async def test_get_work_items_ids_all(devops_client: DevOpsClient) -> None:
    """Test the get_work_items_ids method."""
    work_items_ids = await devops_client.get_work_items_ids_all(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert isinstance(work_items_ids, DevOpsWiqlResult)


@pytest.mark.asyncio
async def test_get_work_items(devops_client: DevOpsClient) -> None:
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
