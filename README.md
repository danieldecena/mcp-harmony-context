# MCP Harmony Context

An MCP (Model Context Protocol) server that provides context about Toon Boom Harmony and its scripting API. This server allows AI assistants to access Harmony's API documentation and help developers work with Harmony's scripting capabilities.

---

## Author

**Jorge Hernandez Ibañez**
Copyright (c) 2025

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Overview

The MCP Harmony Context server exposes Harmony's API documentation through the Model Context Protocol, making it easy for AI assistants to provide accurate information about Harmony's scripting API. The server reads from your local Harmony installation's help documentation and provides it in a clean, accessible format.

### Features

- **API Class Discovery**: Browse all available Harmony API classes with descriptions
- **Class Documentation**: Get detailed documentation for any Harmony API class
- **Search**: Keyword search across class names and descriptions (`search_api` tool)
- **Demo Scripts Access**: Browse and read Harmony's Script API demo `.js` files
- **Diagnostics**: `harmony://config/diagnostics` reports which configured paths exist
- **Works without a local Harmony install**: mirror the public docs with the bundled `scripts/fetch_harmony_docs.py`

---

## Requirements

- **Python 3.12 or higher**
- **Toon Boom Harmony** installed locally (for access to API documentation)
- **uv** package manager (recommended) or pip

### Dependencies

The following Python packages are required:

- `mcp[cli]>=1.18.0` - Model Context Protocol framework with CLI support
- `python-dotenv>=1.0.0` - Environment variable management
- `beautifulsoup4>=4.12.0` - HTML parsing
- `html2text>=2024.2.26` - HTML to markdown conversion

---

## Installation

### 1. Install uv (recomended)

We recommend using [uv](https://docs.astral.sh/uv/) to manage the mcp project.

### 2. Clone the repository

```bash
git clone https://github.com/yourusername/mcp-harmony-context.git
cd mcp-harmony-context
```

### 3. Install dependencies

```bash
uv sync
```

Alternatively, using pip:

```bash
pip install -r requirements.txt
# Or install dependencies directly:
pip install "mcp[cli]>=1.18.0" python-dotenv beautifulsoup4 html2text
```

### 4. Configure the Harmony help path

The server reads documentation HTML from a `help/` folder. You have two options:

#### Option A — Point at your local Harmony install

If Harmony is installed, set `HARMONY_HELP_PATH` to its `help/` directory.

| OS | Typical path |
| --- | --- |
| macOS | `/Applications/Toon Boom Harmony <version> <edition>/Harmony <version> <edition>.app/Contents/tba/resources/help` |
| Windows | `C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony <version> <edition>\help` |
| Linux | `/opt/ToonBoomAnimation/harmony/resources/help` |

On macOS the default auto-discovers any `Toon Boom Harmony*` app under `/Applications/`. On other OSes you usually need to set `HARMONY_HELP_PATH` explicitly.

The simplest config is a `.env` file in the project root:

```bash
HARMONY_HELP_PATH=/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help
```

Or export it inline:

```bash
# macOS / Linux
export HARMONY_HELP_PATH="/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"

# Windows PowerShell
$env:HARMONY_HELP_PATH = "C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help"
```

#### Option B — Mirror the public docs (no Harmony install required)

If you don't have Harmony locally, download the public scripting reference:

```bash
uv run scripts/fetch_harmony_docs.py            # Harmony 25 (default)
uv run scripts/fetch_harmony_docs.py --version 22
```

This mirrors `https://docs.toonboom.com/help/harmony-<version>/scripting/script/` into `./harmony-help/script/` (~5 MB, ~130 class pages, gitignored). Then point `.env` at it:

```bash
HARMONY_HELP_PATH=/absolute/path/to/mcp-harmony-context/harmony-help
```

Demo scripts (`extended/ScriptAPIDemos/`) are not in the online docs — they ship only with Harmony itself.

#### Verify your configuration

On startup the server prints a diagnostic banner to stderr showing whether each required path resolved. You can also query it any time via the `harmony://config/diagnostics` resource.

## Usage

### Running the MCP Server

Start the server using uv:

```bash
uv run main.py
```

Or with Python directly:

```bash
python main.py
```

### Testing with MCP Inspector

You can test the server interactively using the MCP inspector:

```bash
mcp dev main.py
```

This will open an interactive interface where you can explore available resources and tools.

### Integrating with Claude Desktop

Add the server to your Claude Desktop config:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

macOS example:

```json
{
  "mcpServers": {
    "harmony-context": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/mcp-harmony-context", "run", "main.py"],
      "env": {
        "HARMONY_HELP_PATH": "/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"
      }
    }
  }
}
```

Windows example:

```json
{
  "mcpServers": {
    "harmony-context": {
      "command": "uv",
      "args": ["--directory", "C:\\path\\to\\mcp-harmony-context", "run", "main.py"],
      "env": {
        "HARMONY_HELP_PATH": "C:\\Program Files (x86)\\Toon Boom Animation\\Toon Boom Harmony 25 Essentials\\help"
      }
    }
  }
}
```

Replace the `--directory` path with your clone, and `HARMONY_HELP_PATH` with either your Harmony install or the path printed by `scripts/fetch_harmony_docs.py`.

### Using with Other MCP Clients

This server follows the standard MCP protocol and can be integrated with any MCP-compatible client. Refer to your client's documentation for specific integration instructions.

---

## Available Resources

| Resource | Purpose |
| --- | --- |
| `harmony://api/classes` | List every Harmony API class with descriptions |
| `harmony://api/class/{class_name}` | Full documentation for a specific class (e.g. `scene`, `Action`, `Color`) |
| `harmony://config/diagnostics` | Report which configured paths exist; first thing to check when something looks wrong |
| `harmony://config/scripts-demo-path` | Configured path to Harmony's `ScriptAPIDemos/` folder |

## Available Tools

| Tool | Purpose |
| --- | --- |
| `get_class_docs(class_name)` | Same content as `harmony://api/class/{class_name}`, callable as a tool |
| `search_api(query)` | Keyword search across class names and descriptions |
| `list_demo_scripts()` | List every `.js` file under `ScriptAPIDemos/` |
| `get_script_demo(script_name)` | Read a specific demo script as fenced JavaScript |

---

## Project Structure

```text
mcp-harmony-context/
├── main.py                          # MCP server
├── scripts/fetch_harmony_docs.py    # Mirror the public docs locally
├── tests/                           # Pytest suite + fixture HTML
├── pyproject.toml                   # Dependencies and pytest config
├── uv.lock                          # Locked dependency versions
├── LICENSE
├── README.md
├── CLAUDE.md                        # Notes for Claude Code
└── .env                             # HARMONY_HELP_PATH (gitignored)
```

---

## Development

### Prerequisites

- Python 3.12+
- uv package manager
- Either Toon Boom Harmony installed, or run `scripts/fetch_harmony_docs.py` to mirror the public docs

### Setup for Development

1. Clone the repository
2. Run `uv sync` to install dependencies (`uv sync --dev` to include pytest)
3. Configure `HARMONY_HELP_PATH` (see "Configure the Harmony help path" above)
4. Run `mcp dev main.py` to inspect resources and tools interactively

### Running tests

```bash
uv run pytest
```

Tests use fixture HTML under `tests/fixtures/help/` and do **not** require a Harmony install.

### Smoke-test checklist

When picking the project up after a while or on a new machine:

- [ ] `uv sync --dev` succeeds
- [ ] `uv run pytest` is green
- [ ] `uv run main.py` prints `**Status:** OK` in its startup banner
- [ ] `mcp dev main.py` lists `harmony://api/classes`, `harmony://api/class/{class_name}`, `harmony://config/diagnostics`
- [ ] `harmony://api/classes` returns ≥100 classes for a Harmony 25 install/mirror
- [ ] `harmony://api/class/scene` includes a `setStopFrame` mention

### Code Structure

The server is built using FastMCP and follows these conventions:

- **Resources**: Defined with `@mcp.resource()` decorator
- **Tools**: Defined with `@mcp.tool()` decorator (extensible)
- **URI Pattern**: Resources use `harmony://` scheme with hierarchical paths

---

## Troubleshooting

### "Script path does not exist" Error

**Problem**: The server can't find your Harmony help documentation.

**Solution**:

1. Verify your Harmony installation path
2. Check that the help folder exists at that location
3. Update your `HARMONY_HELP_PATH` environment variable or `.env` file

### "No classes found" Error

**Problem**: The server can't parse the API class list.

**Solution**:

1. Ensure your Harmony installation includes the script documentation
2. Check that `annotated.html` exists in the script folder
3. Verify you have read permissions for the help folder

### Import Errors

**Problem**: Missing Python dependencies.

**Solution**:

```bash
uv sync
# Or
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

---

## Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) - A framework for building MCP servers
- Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- Uses [html2text](https://github.com/Alir3z4/html2text/) for markdown conversion

---

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/jorgehi/mcp-harmony-context).
Developer contact: [info@jorgehi.com](mailto:info@jorgehi.com)

---

## Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Toon Boom Harmony](https://www.toonboom.com/products/harmony)
- [Harmony Scripting Documentation](https://docs.toonboom.com/)
