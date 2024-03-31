"""Setup for tests."""

from __future__ import annotations

from typing import Final

ORGANIZATION: Final[str] = "testorg"
PROJECT: Final[str] = "testproject"
PAT: Final[str] = "testpat"

RESPONSE_JSON_BASIC = {"test": "test"}

RESPONSE_JSON_DEVOPS_PROJECT = {
    "id": "testid",
    "name": "testname",
    "description": "testdescription",
    "url": "testurl",
    "state": "teststate",
    "revision": 1,
    "visibility": "testvisibility",
    "last_updated": None,
    "default_team": None,
    "links": None,
}
