"""Mirror Toon Boom Harmony's public scripting reference into ./harmony-help/.

Usage:
    uv run scripts/fetch_harmony_docs.py            # Harmony 25 (default)
    uv run scripts/fetch_harmony_docs.py --version 22

Downloads annotated.html + every classXxx.html it links to, plus the small
set of doxygen CSS/JS files referenced by the pages. Throttled (0.15s between
requests) so we don't hammer docs.toonboom.com.

After it finishes, point HARMONY_HELP_PATH at the local copy:
    HARMONY_HELP_PATH=$(pwd)/harmony-help
"""

from __future__ import annotations

import argparse
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

UA = "mcp-harmony-context docs mirror (https://github.com/jorgehi/mcp-harmony-context)"
THROTTLE_SEC = 0.15
ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "harmony-help" / "script"


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def save(rel_name: str, data: bytes) -> Path:
    out = OUT_DIR / rel_name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(data)
    return out


def discover_class_pages(annotated_html: bytes) -> list[str]:
    """Return the list of class*.html filenames linked from annotated.html."""
    soup = BeautifulSoup(annotated_html, "html.parser")
    table = soup.find("table", class_="directory")
    if not table:
        raise SystemExit("annotated.html has no <table class='directory'>")
    pages: list[str] = []
    seen: set[str] = set()
    for link in table.find_all("a", class_="el"):
        href = link.get("href")
        if not href or href.startswith(("http://", "https://", "#")):
            continue
        # Strip any fragment.
        href = href.split("#", 1)[0]
        if href and href not in seen:
            seen.add(href)
            pages.append(href)
    return pages


def discover_assets(html: bytes, base_url: str) -> set[str]:
    """Return relative URLs for doxygen CSS/JS that pages reference."""
    soup = BeautifulSoup(html, "html.parser")
    assets: set[str] = set()
    for tag, attr in (("link", "href"), ("script", "src"), ("img", "src")):
        for el in soup.find_all(tag):
            ref = el.get(attr)
            if not ref or ref.startswith(("http://", "https://", "data:", "#")):
                continue
            # Only same-directory relative paths (doxygen ships everything flat).
            if "/" in urlparse(ref).path.lstrip("/"):
                continue
            assets.add(ref.split("?", 1)[0])
    return assets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="25", help="Harmony major version (default: 25)")
    parser.add_argument(
        "--base",
        default=None,
        help="Override base URL (default: https://docs.toonboom.com/help/harmony-<version>/scripting/script/)",
    )
    args = parser.parse_args()

    base = args.base or f"https://docs.toonboom.com/help/harmony-{args.version}/scripting/script/"
    print(f"Mirroring {base} -> {OUT_DIR}", file=sys.stderr)

    try:
        annotated = fetch(urljoin(base, "annotated.html"))
    except urllib.error.HTTPError as e:
        print(f"Failed to fetch annotated.html: HTTP {e.code}", file=sys.stderr)
        return 1
    save("annotated.html", annotated)
    print("  annotated.html (1)", file=sys.stderr)

    pages = discover_class_pages(annotated)
    print(f"Found {len(pages)} class pages", file=sys.stderr)

    # Download every class page and collect referenced assets along the way.
    asset_paths: set[str] = set(discover_assets(annotated, base))
    failures: list[tuple[str, str]] = []
    for i, page in enumerate(pages, 1):
        try:
            data = fetch(urljoin(base, page))
        except urllib.error.HTTPError as e:
            failures.append((page, f"HTTP {e.code}"))
            print(f"  [{i}/{len(pages)}] {page}: HTTP {e.code}", file=sys.stderr)
            continue
        except urllib.error.URLError as e:
            failures.append((page, str(e.reason)))
            print(f"  [{i}/{len(pages)}] {page}: {e.reason}", file=sys.stderr)
            continue
        save(page, data)
        asset_paths.update(discover_assets(data, base))
        if i % 25 == 0 or i == len(pages):
            print(f"  [{i}/{len(pages)}] {page}", file=sys.stderr)
        time.sleep(THROTTLE_SEC)

    # Fetch CSS/JS/images referenced by the pages. Failures here are non-fatal:
    # the MCP server only reads HTML, not stylesheets.
    print(f"Fetching {len(asset_paths)} doxygen assets", file=sys.stderr)
    for asset in sorted(asset_paths):
        try:
            data = fetch(urljoin(base, asset))
        except (urllib.error.HTTPError, urllib.error.URLError):
            continue
        save(asset, data)
        time.sleep(THROTTLE_SEC)

    if failures:
        print(f"\n{len(failures)} class pages failed:", file=sys.stderr)
        for page, reason in failures:
            print(f"  {page}: {reason}", file=sys.stderr)

    print(f"\nDone. {OUT_DIR}", file=sys.stderr)
    print(f"Point HARMONY_HELP_PATH at {OUT_DIR.parent}", file=sys.stderr)
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
