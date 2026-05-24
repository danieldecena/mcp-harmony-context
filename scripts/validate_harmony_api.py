"""Cross-check Harmony JavaScript files against the local docs reference.

Given one or more .js files, extracts every `<Receiver>.<method>(` call where
the receiver is a known Harmony global (scene, node, Timeline, ...) and
reports any method that is NOT documented in harmony-help/script/.

Usage:
    uv run scripts/validate_harmony_api.py harmony-scripts
    uv run scripts/validate_harmony_api.py path/to/MyScript.js [more.js ...]

Local-variable calls (`palette.addNewColor()`, `col.setName()`) can't be
statically resolved and are skipped.

Exit codes:
    0  every resolvable call is documented
    1  unknown methods found (printed with file:line)
    2  reference docs missing (run scripts/fetch_harmony_docs.py first)
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SCRIPT_DIR = ROOT / "harmony-help" / "script"

# Receivers that resolve to a Harmony doxygen class of the same name.
# These come from CLAUDE.md's "USE THESE" list plus what's in harmony-scripts/.
HARMONY_GLOBALS = {
    "scene",
    "node",
    "Timeline",
    "MessageLog",
    "MessageBox",
    "Drawing",
    "PaletteObjectManager",
    "PaletteColor",
    "Action",
    "selection",
    "frame",
    "column",
    "fileMapper",
}

CALL_RE = re.compile(r"\b([A-Za-z_]\w*)\.([A-Za-z_]\w*)\s*\(")


def build_class_index(script_dir: Path) -> dict[str, set[str]]:
    """Map className -> set(methodName) from doxygen class*.html files."""
    if not script_dir.exists():
        raise SystemExit(
            f"Reference docs not found at {script_dir}.\n"
            f"Run `uv run scripts/fetch_harmony_docs.py` first."
        )

    index: dict[str, set[str]] = {}
    for html_file in sorted(script_dir.glob("class*.html")):
        class_name = html_file.stem[len("class") :]
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        methods: set[str] = set()
        # Doxygen self-links: <a class="el" href="classscene.html#anchor">methodName</a>
        for link in soup.find_all("a", class_="el"):
            href = link.get("href", "")
            if not href.startswith(f"{html_file.name}#"):
                continue
            name = link.get_text(strip=True)
            if name.isidentifier():
                methods.add(name)
        if methods:
            index[class_name] = methods
    return index


def scan_calls(js_path: Path) -> list[tuple[int, str, str]]:
    """Return [(line_no, receiver, method)] for every Receiver.method( call."""
    out: list[tuple[int, str, str]] = []
    for lineno, line in enumerate(js_path.read_text(encoding="utf-8").splitlines(), 1):
        # Skip lines that are entirely a JS comment.
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        for match in CALL_RE.finditer(line):
            out.append((lineno, match.group(1), match.group(2)))
    return out


def validate(js_paths: list[Path], index: dict[str, set[str]]) -> int:
    unknown: list[tuple[Path, int, str, str]] = []
    skipped_locals: dict[Path, set[str]] = defaultdict(set)
    checked = 0

    for js in js_paths:
        for lineno, recv, method in scan_calls(js):
            if recv not in HARMONY_GLOBALS:
                skipped_locals[js].add(recv)
                continue
            checked += 1
            methods = index.get(recv)
            if methods is None:
                unknown.append((js, lineno, recv, method))
                continue
            if method not in methods:
                unknown.append((js, lineno, recv, method))

    if unknown:
        print(f"Unknown Harmony API calls ({len(unknown)}):")
        for js, lineno, recv, method in unknown:
            print(f"  {js}:{lineno}  {recv}.{method}()")
    else:
        print(f"All {checked} resolvable Harmony API calls are documented.")

    if skipped_locals:
        print("\nSkipped (local-variable receivers, cannot resolve statically):")
        for js, names in sorted(skipped_locals.items()):
            print(f"  {js.name}: {', '.join(sorted(names))}")

    return 1 if unknown else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="+",
        help="One or more .js files or directories containing .js files.",
    )
    parser.add_argument(
        "--script-dir",
        type=Path,
        default=DEFAULT_SCRIPT_DIR,
        help=f"Path to doxygen class*.html (default: {DEFAULT_SCRIPT_DIR})",
    )
    args = parser.parse_args()

    js_paths: list[Path] = []
    for raw in args.targets:
        p = Path(raw)
        if p.is_dir():
            js_paths.extend(sorted(p.glob("*.js")))
        elif p.is_file():
            js_paths.append(p)
        else:
            print(f"Not a file or directory: {p}", file=sys.stderr)
            return 2
    if not js_paths:
        print("No .js files to check.", file=sys.stderr)
        return 2

    try:
        index = build_class_index(args.script_dir)
    except SystemExit as e:
        print(e, file=sys.stderr)
        return 2

    print(f"Reference: {len(index)} classes from {args.script_dir}")
    print(f"Checking : {len(js_paths)} script(s)\n")
    return validate(js_paths, index)


if __name__ == "__main__":
    raise SystemExit(main())
