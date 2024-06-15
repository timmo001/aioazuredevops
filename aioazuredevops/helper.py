"""Helper functions for Azure DevOps."""

from dataclasses import dataclass

from .models.iteration import Iteration, IterationTimeFrame
from .models.work_item import WorkItem
from .models.work_item_type import Category, State, WorkItemType


def current_iteration(iterations: list[Iteration]) -> Iteration | None:
    """Get current iteration."""
    for iteration in iterations:
        if iteration.attributes.time_frame == IterationTimeFrame.CURRENT:
            return iteration
    return None


def previous_iteration(iterations: list[Iteration]) -> Iteration | None:
    """Get previous iteration."""
    for key, iteration in enumerate(iterations):
        if iteration.attributes.time_frame == IterationTimeFrame.CURRENT:
            return iterations[key - 1]
    return None


def next_iteration(iterations: list[Iteration]) -> Iteration | None:
    """Get next iteration."""
    for key, iteration in enumerate(iterations):
        if iteration.attributes.time_frame == IterationTimeFrame.CURRENT:
            return iterations[key + 1]
    return None


@dataclass
class WorkItemState(State):
    """Work item by type and state."""

    work_items: list[WorkItem]


@dataclass
class WorkItemTypeAndState(WorkItemType):
    """Work item by type and state."""

    state_items: list[WorkItemState]


def work_item_types_states_filter(
    work_item_types: list[WorkItemType],
    categories: list[Category] | None = None,
    ignored_categories: list[Category] | None = None,
) -> list[str]:
    """Get states filter by category."""
    if categories is None and ignored_categories is None:
        return []

    states = []
    for work_item_type in work_item_types:
        for state in work_item_type.states:
            if categories is not None and state.category in categories:
                states.append(state.name)
            elif (
                ignored_categories is not None
                and state.category not in ignored_categories
            ):
                states.append(state.name)
    return states


def work_items_by_type_and_state(
    work_item_types: list[WorkItemType],
    work_items: list[WorkItem],
    categories: list[Category] | None = None,
    ignored_categories: list[Category] | None = None,
) -> list[WorkItemTypeAndState]:
    """Get work items by type and state."""

    result: list[WorkItemTypeAndState] = []
    for work_item_type in work_item_types:
        states: list[WorkItemState] = []
        for state in work_item_type.states:
            items = [item for item in work_items if item.fields.state == state.name]
            state = WorkItemState(
                name=state.name,
                color=state.color,
                category=state.category,
                work_items=items,
            )
            if categories is not None and state.category in categories:
                states.append(state)
            elif (
                ignored_categories is not None
                and state.category not in ignored_categories
            ):
                states.append(state)
        result.append(
            WorkItemTypeAndState(
                name=work_item_type.name,
                reference_name=work_item_type.reference_name,
                description=work_item_type.description,
                color=work_item_type.color,
                icon=work_item_type.icon,
                is_disabled=work_item_type.is_disabled,
                xml_form=work_item_type.xml_form,
                fields=work_item_type.fields,
                field_instances=work_item_type.field_instances,
                transitions=work_item_type.transitions,
                states=work_item_type.states,
                url=work_item_type.url,
                state_items=states,
            )
        )

    return result
