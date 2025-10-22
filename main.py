"""
MCP server for providing context about Harmony and their API.
"""

import os
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

# Configuration: Harmony help documentation path
# Set via environment variable or use default
HARMONY_HELP_PATH = os.getenv(
    "HARMONY_HELP_PATH",
    r"C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help"
)

def get_harmony_help_path() -> Path:
    """Get the configured Harmony help documentation path."""
    return Path(HARMONY_HELP_PATH)


def get_script_path() -> Path:
    """Get the script documentation folder path."""
    return get_harmony_help_path() / "script"


def get_available_classes() -> List[dict]:
    """Get list of all available API classes with descriptions from annotated.html.

    Returns:
        List of dicts with 'name' and 'description' keys.
    """
    script_path = get_script_path()
    annotated_file = script_path / "annotated.html"

    if not annotated_file.exists():
        return []

    try:
        html_content = annotated_file.read_text(encoding="utf-8")
        soup = BeautifulSoup(html_content, 'html.parser')

        classes = []

        # Find all table rows in the class list
        table = soup.find('table', class_='directory')
        if not table:
            return []

        for row in table.find_all('tr'):
            # Find the class name link
            link = row.find('a', class_='el')
            if not link:
                continue

            class_name = link.get_text(strip=True)

            # Find the description
            desc_td = row.find('td', class_='desc')
            if desc_td:
                # Convert HTML to text
                h = html2text.HTML2Text()
                h.ignore_links = True
                h.ignore_images = True
                h.ignore_emphasis = False
                h.body_width = 0
                description = h.handle(str(desc_td)).strip()
            else:
                description = ""

            classes.append({
                'name': class_name,
                'description': description
            })

        return sorted(classes, key=lambda x: x['name'].lower())

    except Exception as e:
        return []


@mcp.resource("harmony://api/classes")
def get_classes() -> str:
    """Get list of all available Harmony API classes with descriptions.

    Returns a list of class names and brief descriptions that can be queried for full documentation.
    """
    classes = get_available_classes()

    if not classes:
        script_path = get_script_path()
        return f"No classes found. Please check that the script path exists: {script_path}"

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
        return f"Error: Script path does not exist: {script_path}"

    # Construct the filename: class{ClassName}.html
    html_file = script_path / f"class{class_name}.html"

    if not html_file.exists():
        # Try to find similar class names for helpful error message
        available = get_available_classes()
        similar = [c for c in available if class_name.lower() in c['name'].lower()]

        error_msg = f"Error: Class '{class_name}' not found.\n\n"
        if similar:
            error_msg += f"Did you mean one of these?\n"
            error_msg += "\n".join(f"  - {c['name']}: {c['description'][:80]}..." if len(c['description']) > 80 else f"  - {c['name']}: {c['description']}" for c in similar[:5])
        else:
            error_msg += f"Use harmony://api/classes to see all available classes."

        return error_msg

    # Read and process the HTML content
    try:
        html_content = html_file.read_text(encoding="utf-8")

        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract only the doc-content div
        doc_content = soup.find('div', id='doc-content')

        if not doc_content:
            # Fallback if doc-content div not found
            return f"Warning: Could not find documentation content in {html_file}"

        # Convert HTML to clean markdown/text
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = True
        h.ignore_emphasis = False
        h.body_width = 0  # Don't wrap lines

        clean_text = h.handle(str(doc_content))

        return f"# {class_name} Class Documentation\n\n{clean_text}"

    except Exception as e:
        return f"Error reading file {html_file}: {str(e)}"


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
