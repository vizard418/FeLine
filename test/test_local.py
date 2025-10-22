#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import pytest
from pathlib import Path
from lib.local import Local


@pytest.mark.parametrize(
    "mock_platform,expected_subpath",
    [
        ("win32", ["AppData", ".cache", "FeLine"]),
        ("darwin", ["Library", "Caches", "FeLine"]),
        ("linux", [".cache", "FeLine"]),
    ],
)
def test_hist_path_for_all_platforms(monkeypatch, tmp_path, mock_platform, expected_subpath):
    # patch the platform in the module where Local is defined
    monkeypatch.setattr(Local.__module__ + ".platform", mock_platform)
    # patch the home directory so no filesystem is touched
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    local = Local()
    hist_path = local.get_hist_path()

    # Check path parts
    for part in expected_subpath:
        assert part in hist_path.parts
    # Check file name
    assert hist_path.name == ".history"

