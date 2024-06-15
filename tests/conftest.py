"""Fixtures for testing."""

from collections.abc import AsyncGenerator

from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest

from aioazuredevops.client import DEFAULT_API_VERSION, DEFAULT_BASE_URL, DevOpsClient

from . import (
    ORGANIZATION,
    PROJECT,
    RESPONSE_JSON_BASIC,
    RESPONSE_JSON_DEVOPS_BUILD,
    RESPONSE_JSON_DEVOPS_BUILDS,
    RESPONSE_JSON_DEVOPS_ITERATION,
    RESPONSE_JSON_DEVOPS_ITERATION_WORK_ITEMS,
    RESPONSE_JSON_DEVOPS_ITERATIONS,
    RESPONSE_JSON_DEVOPS_PROJECT,
    RESPONSE_JSON_DEVOPS_WIQL_RESULT,
    RESPONSE_JSON_DEVOPS_WORK_ITEM,
    RESPONSE_JSON_DEVOPS_WORK_ITEM_TYPES,
    RESPONSE_JSON_DEVOPS_WORK_ITEMS,
)


@pytest.fixture(autouse=True)
def mock_aioresponse():
    """Return a client session."""
    with aioresponses() as mocker:
        mocker.get(
            f"{DEFAULT_BASE_URL}/",
            payload=RESPONSE_JSON_BASIC,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis/projects?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/_apis/projects/{PROJECT}?api-version={DEFAULT_API_VERSION}&includeCapabilities=true&includeHistory=true",
            payload=RESPONSE_JSON_DEVOPS_PROJECT,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/build/builds?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_BUILDS,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/build/builds/1?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_BUILD,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/work/teamsettings/iterations?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_ITERATIONS,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/work/teamsettings/iterations/abc123?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_ITERATION,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/work/teamsettings/iterations/abc123/workitems?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_ITERATION_WORK_ITEMS,
            status=200,
            repeat=True,
        )
        mocker.post(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/wiql?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_WIQL_RESULT,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems?api-version={DEFAULT_API_VERSION}&errorPolicy=omit&ids=1",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEMS,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems?api-version={DEFAULT_API_VERSION}&errorPolicy=omit&ids={'%252C'.join(str(i) for i in [1]*200)}",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEMS,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems?api-version={DEFAULT_API_VERSION}&errorPolicy=omit&ids={'%252C'.join(str(i) for i in [1]*100)}",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEMS,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems/1?api-version={DEFAULT_API_VERSION}&errorPolicy=omit",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEM,
            status=200,
            repeat=True,
        )
        mocker.get(
            f"{DEFAULT_BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitemtypes?api-version={DEFAULT_API_VERSION}",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEM_TYPES,
            status=200,
            repeat=True,
        )

        yield mocker


@pytest.fixture
async def devops_client() -> AsyncGenerator[DevOpsClient, None]:
    """Return a DevOpsClient."""
    async with ClientSession() as session:
        yield DevOpsClient(session=session)
