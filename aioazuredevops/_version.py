"""Version helper for aioazuredevops.

Expose a simple string value for the current package version,
to remove the dependency on incremental and its auto-generated file.
"""

from __future__ import annotations

try:
    # Prefer to derive version from setup.py via importlib.metadata when installed
    from importlib.metadata import version as _dist_version

    __version__ = _dist_version("aioazuredevops")
except Exception:  # pragma: no cover - fallback to static string if not installed
    # Keep in sync with setup.py
    __version__ = "2.2.2.dev0"

__all__ = ["__version__"]
