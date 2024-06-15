"""Test helpers."""

from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion

from aioazuredevops.client import DevOpsClient
from aioazuredevops.helper import (
    work_item_types_states_filter,
    work_items_by_type_and_state,
)
from aioazuredevops.models.work_item_types import Category

from . import ORGANIZATION, PROJECT


@pytest.mark.asyncio
async def test_work_item_types_states_filter(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_work_item_types method."""
    work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert work_item_types is not None

    assert work_item_types_states_filter(work_item_types) == snapshot(name="no_filter")

    assert (
        work_item_types_states_filter(
            work_item_types,
            categories=[Category.IN_PROGRESS],
            ignored_categories=[Category.COMPLETED, Category.REMOVED],
        )
        == snapshot()
    )


@pytest.mark.asyncio
async def test_work_items_by_type_and_state(
    devops_client: DevOpsClient,
    mock_aioresponse: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test the get_work_item_types method."""
    work_item_types = await devops_client.get_work_item_types(
        organization=ORGANIZATION,
        project=PROJECT,
    )

    assert work_item_types is not None

    work_item_ids = await devops_client.get_work_item_ids(
        organization=ORGANIZATION,
        project=PROJECT,
        states=work_item_types_states_filter(work_item_types),
    )

    assert work_item_ids is not None

    work_items = await devops_client.get_work_items(
        organization=ORGANIZATION,
        project=PROJECT,
        ids=work_item_ids,
    )

    assert work_items is not None

    assert (
        work_items_by_type_and_state(
            work_item_types,
            work_items,
            categories=[Category.IN_PROGRESS],
            ignored_categories=[Category.COMPLETED, Category.REMOVED],
        )
        == snapshot()
    )
