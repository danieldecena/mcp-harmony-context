"""Tests for the mcp-harmony-context server.

These run entirely off fixture HTML in tests/fixtures/help — they do not
require a Toon Boom Harmony install.
"""

from __future__ import annotations

import pytest


def test_get_available_classes_parses_and_sorts(main_module):
    classes = main_module.get_available_classes()
    names = [c["name"] for c in classes]
    assert names == sorted(names, key=str.lower)
    assert {"scene", "Action", "Color", "node"} <= set(names)

    by_name = {c["name"]: c for c in classes}
    assert "Scene-level functions" in by_name["scene"]["description"]
    # Rows missing a <td class="desc"> get an empty description, not a crash.
    assert by_name["node"]["description"] == ""


def test_missing_annotated_html_raises(main_with_path, tmp_path):
    main = main_with_path(tmp_path)
    with pytest.raises(main.HarmonyPathError, match="annotated.html not found"):
        main.get_available_classes()


def test_malformed_annotated_html_raises(main_with_path, tmp_path):
    script = tmp_path / "script"
    script.mkdir()
    (script / "annotated.html").write_text("<html><body>no table here</body></html>")
    main = main_with_path(tmp_path)
    with pytest.raises(main.HarmonyPathError, match="no <table class='directory'>"):
        main.get_available_classes()


def test_validate_paths_ok_with_fixtures(main_module):
    report = main_module.validate_harmony_paths()
    assert report["ok"] is True
    assert report["source"] == "HARMONY_HELP_PATH env var"
    labels = {c["label"]: c for c in report["checks"]}
    assert labels["script/annotated.html"]["exists"] is True
    assert labels["extended/ScriptAPIDemos/"]["exists"] is True


def test_validate_paths_not_ok_when_missing(main_with_path, tmp_path):
    main = main_with_path(tmp_path / "nope")
    report = main.validate_harmony_paths()
    assert report["ok"] is False
    assert any(not c["exists"] and c["required"] for c in report["checks"])


def test_get_class_documentation_returns_class_content(main_module):
    doc = main_module.get_class_documentation("scene")
    assert "scene Class Documentation" in doc
    assert "setStopFrame" in doc
    # The top-level header div outside doc-content must be filtered out.
    assert "irrelevant header" not in doc


def test_get_class_documentation_unknown_class_suggests_similar(main_module):
    doc = main_module.get_class_documentation("scen")  # typo near 'scene'
    assert "not found" in doc
    assert "scene" in doc.lower()


def test_get_class_documentation_missing_script_path(main_with_path, tmp_path):
    main = main_with_path(tmp_path / "no-such-help")
    out = main.get_class_documentation("scene")
    assert "Harmony API not available" in out
    assert "diagnostics" in out


def test_get_class_documentation_handles_missing_doc_content(main_with_path, tmp_path):
    script = tmp_path / "script"
    script.mkdir()
    (script / "annotated.html").write_text(
        "<html><body><table class='directory'></table></body></html>"
    )
    (script / "classBroken.html").write_text("<html><body>no doc-content div here</body></html>")
    main = main_with_path(tmp_path)
    out = main.get_class_documentation("Broken")
    assert "format unexpected" in out
    assert "classBroken.html" in out


def test_get_classes_resource_lists_all(main_module):
    out = main_module.get_classes()
    assert "Available Harmony API Classes (4 total)" in out
    for name in ("scene", "Action", "Color", "node"):
        assert f"## {name}" in out


def test_get_classes_resource_reports_misconfigured(main_with_path, tmp_path):
    main = main_with_path(tmp_path)
    out = main.get_classes()
    assert "Harmony API not available" in out
    assert "harmony://config/diagnostics" in out


def test_search_api_matches_name_and_description(main_module):
    by_name = main_module.search_api("color")
    assert "Color" in by_name

    by_desc = main_module.search_api("frame rate")
    assert "scene" in by_desc

    miss = main_module.search_api("definitely-not-a-thing")
    assert "No classes found" in miss


def test_list_and_get_demo_script(main_module):
    listed = main_module.list_demo_scripts()
    assert "TB_ExportCamera.js" in listed

    body = main_module.get_script_demo("TB_ExportCamera.js")
    assert "```javascript" in body
    assert "exporting camera" in body


def test_diagnostics_resource_renders(main_module):
    out = main_module.get_diagnostics()
    assert "Harmony Context — Diagnostics" in out
    assert "**Status:** OK" in out
