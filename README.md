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
- **Demo Scripts Access**: Access to Harmony's Script API demo files
- **Clean Markdown Output**: HTML documentation converted to readable markdown format

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

### 4. Configure Harmony help path

The server needs to know where your Harmony help documentation is located.

**Option 1: .env File (recomended)**

Create a `.env` file in the project root:

```bash
HARMONY_HELP_PATH=C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help
```

**Default Path**: If not configured, the server defaults to:
`C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help`

---

**Option 2: Environment Variable**

Set the `HARMONY_HELP_PATH` environment variable:

```bash
# Windows (Command Prompt)
set HARMONY_HELP_PATH=C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help

# Windows (PowerShell)
$env:HARMONY_HELP_PATH="C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help"

# macOS/Linux
export HARMONY_HELP_PATH="/Applications/Toon Boom Harmony/help"
```

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

To use this MCP server with Claude Desktop, add it to your Claude configuration file:

**On macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**On Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "harmony-context": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-harmony-context",
        "run",
        "main.py"
      ],
      "env": {
        "HARMONY_HELP_PATH": "C:\\Program Files (x86)\\Toon Boom Animation\\Toon Boom Harmony 25 Essentials\\help"
      }
    }
  }
}
```

Replace `/path/to/mcp-harmony-context` with the actual path to your cloned repository.

### Using with Other MCP Clients

This server follows the standard MCP protocol and can be integrated with any MCP-compatible client. Refer to your client's documentation for specific integration instructions.

---

## Available Resources

Once the server is running, the following resources are available:

### `harmony://api/classes`

Returns a list of all available Harmony API classes with their descriptions.

**Example Response:**

```markdown
# Available Harmony API Classes (150+ total)

## Action
The Action class provides methods for manipulating actions in Harmony...

## Color
The Color class provides methods for working with colors...
```

### `harmony://api/class/{class_name}`

Returns detailed documentation for a specific API class.

**Example:** `harmony://api/class/scene`

**Example Response:**

```markdown
# scene Class Documentation

Detailed documentation including:
- Class description
- Methods and their signatures
- Method parameters and return types
- Usage examples
```

### `harmony://config/scripts-demo-path`

Returns the configured path to Harmony's Script API demo files.

---

## Project Structure

```
mcp-harmony-context/
├── main.py              # Main MCP server implementation
├── pyproject.toml       # Project dependencies and metadata
├── uv.lock              # Locked dependency versions
├── LICENSE              # MIT License
├── README.md            # This file
├── CLAUDE.md            # Development guidance for Claude Code
└── .env                 # Environment configuration (create from .env.example)
```

---

## Development

### Prerequisites

- Python 3.12+
- uv package manager
- Toon Boom Harmony installed

### Setup for Development

1. Clone the repository
2. Run `uv sync` to install dependencies
3. Configure your `HARMONY_HELP_PATH`
4. Run `mcp dev main.py` to test interactively

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
