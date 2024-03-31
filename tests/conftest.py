"""Fixtures for testing."""

from collections.abc import AsyncGenerator

from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest

from aioazuredevops.client import BASE_URL, DevOpsClient

from . import (
    ORGANIZATION,
    PROJECT,
    RESPONSE_JSON_BASIC,
    RESPONSE_JSON_DEVOPS_BUILD,
    RESPONSE_JSON_DEVOPS_BUILDS,
    RESPONSE_JSON_DEVOPS_PROJECT,
    RESPONSE_JSON_DEVOPS_WIQL_RESULT,
    RESPONSE_JSON_DEVOPS_WORK_ITEMS,
)


@pytest.fixture(autouse=True)
def mock_aioresponse():
    """Return a client session."""
    with aioresponses() as mocker:
        mocker.get(
            f"{BASE_URL}/",
            payload=RESPONSE_JSON_BASIC,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/{PROJECT}",
            payload=RESPONSE_JSON_BASIC,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/_apis",
            payload=RESPONSE_JSON_BASIC,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/_apis/projects",
            payload=RESPONSE_JSON_BASIC,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/_apis/projects/{PROJECT}",
            payload=RESPONSE_JSON_DEVOPS_PROJECT,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/build/builds",
            payload=RESPONSE_JSON_DEVOPS_BUILDS,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/build/builds/1",
            payload=RESPONSE_JSON_DEVOPS_BUILD,
            status=200,
        )
        mocker.post(
            f"{BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/wiql?api-version=6.0",
            payload=RESPONSE_JSON_DEVOPS_WIQL_RESULT,
            status=200,
        )
        mocker.get(
            f"{BASE_URL}/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems?ids=1&api-version=6.0",
            payload=RESPONSE_JSON_DEVOPS_WORK_ITEMS,
            status=200,
        )

        yield mocker


@pytest.fixture
async def devops_client() -> AsyncGenerator[DevOpsClient, None]:
    """Return a DevOpsClient."""
    async with ClientSession() as session:
        yield DevOpsClient(session=session)
