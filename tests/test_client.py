"""Test the http client module."""

# from aioresponses import aioresponses
import pytest

from aioazuredevops.client import DevOpsClient
from aioazuredevops.core import DevOpsProject

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
    assert project.project_id == "testid"
    assert project.name == "testname"
    assert project.description == "testdescription"
    assert project.url == "testurl"
    assert project.state == "teststate"
    assert project.revision == 1
    assert project.visibility == "testvisibility"
    assert project.last_updated is None
    assert project.default_team is None
    assert project.links is None
