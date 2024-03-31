"""Setup for tests."""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, Final

from aiohttp.test_utils import TestClient

TOKEN: Final[str] = "abc123"


ClientSessionGenerator = Callable[..., Coroutine[Any, Any, TestClient]]
