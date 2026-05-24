"""Pytest fixtures: point `main` at the bundled fixture help tree.

`main` reads HARMONY_HELP_PATH at import time, so we set the env var here
(before `main` is imported anywhere) and provide a session-scoped reload
hook so individual tests can swap paths.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path

import pytest

FIXTURE_HELP = Path(__file__).parent / "fixtures" / "help"


@pytest.fixture
def fixture_help_path() -> Path:
    return FIXTURE_HELP


@pytest.fixture
def main_module(monkeypatch, fixture_help_path):
    """Import (or re-import) `main` with HARMONY_HELP_PATH pointed at fixtures."""
    monkeypatch.setenv("HARMONY_HELP_PATH", str(fixture_help_path))
    sys.modules.pop("main", None)
    return importlib.import_module("main")


@pytest.fixture
def main_with_path(monkeypatch):
    """Factory: import `main` with an arbitrary HARMONY_HELP_PATH."""

    def _load(path: os.PathLike[str] | str):
        monkeypatch.setenv("HARMONY_HELP_PATH", str(path))
        sys.modules.pop("main", None)
        return importlib.import_module("main")

    return _load
