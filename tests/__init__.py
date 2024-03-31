"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Final

from aiohttp.test_utils import TestClient

ORGANIZATION: Final[str] = "testorg"
PROJECT: Final[str] = "testproject"
PAT: Final[str] = "testpat"


ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]
