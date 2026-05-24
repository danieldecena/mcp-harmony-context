"""
MCP server for providing context about Harmony and their API.

Copyright (c) 2025 Claude
Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""

import os
import platform
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import html2text

# Load environment variables from .env file
load_dotenv()

# Create an MCP server
mcp = FastMCP("mcp-harmony-context")


def _default_harmony_help_path() -> str:
    """Pick a sensible default help-doc path for the host OS.

    Users normally override this with HARMONY_HELP_PATH; these defaults exist
    so the error message at startup points somewhere plausible.
    """
    system = platform.system()
    if system == "Darwin":
        # Newest install wins if several Harmony versions are present.
        candidates = sorted(
            Path("/Applications").glob("Toon Boom Harmony*"),
            reverse=True,
        )
        for app_dir in candidates:
            for app_bundle in app_dir.glob("*.app"):
                help_dir = app_bundle / "Contents" / "tba" / "resources" / "help"
                if help_dir.exists():
                    return str(help_dir)
        return "/Applications/Toon Boom Harmony 25 Premium/Harmony 25 Premium.app/Contents/tba/resources/help"
    if system == "Linux":
        return "/opt/ToonBoomAnimation/harmony/resources/help"
    return r"C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help"


HARMONY_HELP_PATH = os.getenv("HARMONY_HELP_PATH", _default_harmony_help_path())

def get_harmony_help_path() -> Path:
    """Get the configured Harmony help documentation path."""
    return Path(HARMONY_HELP_PATH)


def get_script_path() -> Path:
    """Get the script documentation folder path."""
    return get_harmony_help_path() / "script"


def get_scripts_demo_path() -> Path:
    """Get the scripts demo folder path."""
    return get_harmony_help_path() / "extended" / "ScriptAPIDemos"


class HarmonyPathError(RuntimeError):
    """Raised when the configured Harmony help path is missing or malformed."""


def validate_harmony_paths() -> dict:
    """Inspect every path the server depends on and return a diagnostic report.

    The shape is stable so it can back both the diagnostics resource and the
    startup banner. `ok` is True only when every required path resolves.
    """
    help_path = get_harmony_help_path()
    script_path = get_script_path()
    annotated = script_path / "annotated.html"
    demos = get_scripts_demo_path()

    checks = [
        ("HARMONY_HELP_PATH", help_path, True),
        ("script/", script_path, True),
        ("script/annotated.html", annotated, True),
        ("extended/ScriptAPIDemos/", demos, False),
    ]
    results = [
        {"label": label, "path": str(path), "exists": path.exists(), "required": required}
        for label, path, required in checks
    ]
    return {
        "ok": all(r["exists"] for r in results if r["required"]),
        "source": "HARMONY_HELP_PATH env var" if os.getenv("HARMONY_HELP_PATH") else "built-in default",
        "checks": results,
    }


def _format_diagnostics(report: dict) -> str:
    lines = [
        f"**Status:** {'OK' if report['ok'] else 'MISCONFIGURED'}",
        f"**Source:** {report['source']}",
        "",
        "| Required | Exists | Path |",
        "| -------- | ------ | ---- |",
    ]
    for c in report["checks"]:
        req = "yes" if c["required"] else "no"
        exists = "yes" if c["exists"] else "no"
        lines.append(f"| {req} | {exists} | `{c['path']}` ({c['label']}) |")
    if not report["ok"]:
        lines += [
            "",
            "Set `HARMONY_HELP_PATH` in your `.env` to the `help` folder inside your Harmony install.",
            "On macOS this is typically:",
            "`/Applications/Toon Boom Harmony <version> <edition>/Harmony <version> <edition>.app/Contents/tba/resources/help`",
        ]
    return "\n".join(lines)


def get_available_classes() -> List[dict]:
    """Get list of all available API classes with descriptions from annotated.html.

    Raises:
        HarmonyPathError: if annotated.html is missing or unparseable. Resources
        catch this and surface a readable message rather than an empty list,
        so misconfiguration never looks like "Harmony has zero classes".
    """
    script_path = get_script_path()
    annotated_file = script_path / "annotated.html"

    if not annotated_file.exists():
        raise HarmonyPathError(f"annotated.html not found at {annotated_file}")

    html_content = annotated_file.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "html.parser")

    table = soup.find("table", class_="directory")
    if not table:
        raise HarmonyPathError(
            f"annotated.html at {annotated_file} has no <table class='directory'> — "
            "Harmony help format may have changed."
        )

    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0

    classes = []
    for row in table.find_all("tr"):
        link = row.find("a", class_="el")
        if not link:
            continue
        class_name = link.get_text(strip=True)
        desc_td = row.find("td", class_="desc")
        description = h.handle(str(desc_td)).strip() if desc_td else ""
        classes.append({"name": class_name, "description": description})

    return sorted(classes, key=lambda x: x["name"].lower())


@mcp.resource("harmony://api/classes")
def get_classes() -> str:
    """Get list of all available Harmony API classes with descriptions.

    Returns a list of class names and brief descriptions that can be queried for full documentation.
    """
    try:
        classes = get_available_classes()
    except HarmonyPathError as e:
        return (
            f"# Harmony API not available\n\n{e}\n\n"
            f"Run `harmony://config/diagnostics` for details."
        )

    if not classes:
        return (
            "# No classes found\n\n"
            "annotated.html was readable but contained no class entries. "
            "See `harmony://config/diagnostics` for paths."
        )

    # Return as formatted list with descriptions
    result = f"# Available Harmony API Classes ({len(classes)} total)\n\n"

    for class_info in classes:
        name = class_info['name']
        desc = class_info['description']

        if desc:
            result += f"## {name}\n{desc}\n\n"
        else:
            result += f"## {name}\n\n"

    result += "\n---\n\n"
    result += "To get full documentation for a specific class, use: `harmony://api/class/{className}`\n"

    return result


@mcp.resource("harmony://api/class/{class_name}")
def get_class_documentation(class_name: str) -> str:
    """Get the documentation for a specific Harmony API class.

    Args:
        class_name: Name of the class (e.g., "Action", "Color", "scene")

    Returns:
        Clean, readable documentation for the class, or an error message if not found.
    """
    script_path = get_script_path()

    if not script_path.exists():
        return (
            f"Harmony API not available: script path does not exist ({script_path}).\n"
            f"Run `harmony://config/diagnostics` for details."
        )

    html_file = script_path / f"class{class_name}.html"

    if not html_file.exists():
        try:
            available = get_available_classes()
        except HarmonyPathError:
            available = []
        similar = [c for c in available if class_name.lower() in c["name"].lower()]

        lines = [f"Error: Class '{class_name}' not found."]
        if similar:
            lines.append("\nDid you mean one of these?")
            for c in similar[:5]:
                desc = c["description"]
                if len(desc) > 80:
                    desc = desc[:80] + "..."
                lines.append(f"  - {c['name']}: {desc}" if desc else f"  - {c['name']}")
        else:
            lines.append("\nUse harmony://api/classes to see all available classes.")
        return "\n".join(lines)

    # OSError surfaces if the file is unreadable; UnicodeDecodeError if the
    # encoding assumption breaks. Both are bugs we want to see, not swallow.
    try:
        html_content = html_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        return f"Error reading {html_file.name}: {e}"

    soup = BeautifulSoup(html_content, "html.parser")
    doc_content = soup.find("div", id="doc-content")
    if not doc_content:
        return (
            f"Harmony class page format unexpected: no <div id='doc-content'> in {html_file.name}. "
            f"Run `harmony://config/diagnostics` if this is widespread."
        )

    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True
    h.ignore_emphasis = False
    h.body_width = 0

    return f"# {class_name} Class Documentation\n\n{h.handle(str(doc_content))}"


@mcp.resource("harmony://config/diagnostics")
def get_diagnostics() -> str:
    """Report which configured paths exist and whether the server is usable."""
    return "# Harmony Context — Diagnostics\n\n" + _format_diagnostics(validate_harmony_paths())


@mcp.resource("harmony://config/scripts-demo-path")
def get_scripts_demo_path_resource() -> str:
    """Get the path to the Harmony scripts demo folder.

    Returns the configured path to the ScriptAPIDemos folder and whether it exists.
    """
    scripts_demo_path = get_scripts_demo_path()
    exists = scripts_demo_path.exists()

    result = f"# Harmony Scripts Demo Path\n\n"
    result += f"**Path:** `{scripts_demo_path}`\n\n"
    result += f"**Exists:** {'Yes' if exists else 'No'}\n\n"

    if not exists:
        result += "⚠️ **Warning:** The scripts demo path does not exist. "
        result += "Please check your HARMONY_HELP_PATH configuration.\n"

    return result


@mcp.tool()
def get_class_docs(class_name: str) -> str:
    """Get full documentation for a specific Harmony API class.

    Args:
        class_name: Name of the class (e.g., "Action", "Color", "scene")
    """
    return get_class_documentation(class_name)


@mcp.tool()
def search_api(query: str) -> str:
    """Search across all Harmony API class names and descriptions for a keyword or concept.

    Args:
        query: Keyword or concept to search for
    """
    try:
        classes = get_available_classes()
    except HarmonyPathError as e:
        return f"Harmony API not available: {e}\nRun `harmony://config/diagnostics` for details."
    if not classes:
        return "No classes parsed from annotated.html — see `harmony://config/diagnostics`."

    query_lower = query.lower()
    matches = [
        c for c in classes
        if query_lower in c['name'].lower() or query_lower in c['description'].lower()
    ]

    if not matches:
        return f"No classes found matching '{query}'."

    result = f"# Search Results for '{query}' ({len(matches)} found)\n\n"
    for c in matches:
        desc = c['description']
        result += f"## {c['name']}\n{desc}\n\n" if desc else f"## {c['name']}\n\n"
    result += "---\nUse `get_class_docs(class_name)` to get full documentation for any class.\n"
    return result


@mcp.tool()
def list_demo_scripts() -> str:
    """List all available demo scripts in the Harmony ScriptAPIDemos folder."""
    demos_path = get_scripts_demo_path()

    if not demos_path.exists():
        return f"ScriptAPIDemos folder not found at: {demos_path}"

    scripts = sorted(demos_path.rglob("*.js")) + sorted(demos_path.rglob("*.zip"))
    js_scripts = sorted(demos_path.rglob("*.js"))

    if not js_scripts:
        return f"No demo scripts found in: {demos_path}"

    result = f"# Harmony Script API Demos ({len(js_scripts)} scripts)\n\n"
    for script in js_scripts:
        relative = script.relative_to(demos_path)
        result += f"- `{relative}`\n"
    result += "\n---\nUse `get_script_demo(script_name)` to read a specific script.\n"
    return result


@mcp.tool()
def get_script_demo(script_name: str) -> str:
    """Read and return the content of a specific Harmony demo script.

    Args:
        script_name: Script filename or relative path (e.g., "TB_ExportCamera.js")
    """
    demos_path = get_scripts_demo_path()

    if not demos_path.exists():
        return f"ScriptAPIDemos folder not found at: {demos_path}"

    # Search for the script by name
    matches = list(demos_path.rglob(script_name))
    if not matches:
        # Try without extension
        matches = list(demos_path.rglob(f"{script_name}.js"))

    if not matches:
        return f"Script '{script_name}' not found. Use `list_demo_scripts()` to see available scripts."

    script_file = matches[0]
    try:
        content = script_file.read_text(encoding="utf-8")
        return f"# {script_file.name}\n\n```javascript\n{content}\n```"
    except Exception as e:
        return f"Error reading script {script_file}: {e}"


if __name__ == "__main__":
    # MCP uses stdout for protocol traffic — never print diagnostics there.
    import sys

    report = validate_harmony_paths()
    print(_format_diagnostics(report), file=sys.stderr)
    print("", file=sys.stderr)
    mcp.run()
