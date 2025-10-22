# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server that provides context about Harmony and their API. The server is built using FastMCP and exposes resources and tools to help AI assistants understand and interact with Harmony's ecosystem.

## Technology Stack

- **Python 3.12+**: Required Python version
- **FastMCP**: Framework for building MCP servers (mcp[cli]>=1.18.0)
- **uv**: Package manager for Python dependencies

## Configuration

The server requires configuration to point to the Harmony help documentation folder.

### Environment Variable
Set the `HARMONY_HELP_PATH` environment variable to your Harmony installation help folder:

```bash
# Windows example
set HARMONY_HELP_PATH=C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help

# Or use .env file (copy .env.example to .env and modify)
```

The default path is: `C:\Program Files (x86)\Toon Boom Animation\Toon Boom Harmony 25 Essentials\help`

## Development Commands

### Setup and Installation
```bash
# Install dependencies using uv
uv sync

# Configure your Harmony help path (optional if using default)
# Copy .env.example to .env and update HARMONY_HELP_PATH

# Run the MCP server
uv run main.py
```

### Testing the Server
```bash
# Use MCP inspector to test the server interactively
mcp dev main.py
```

## Architecture

### Core Structure

- **main.py**: Entry point containing the FastMCP server instance and all resource/tool definitions
- The server is registered as "mcp-harmony-context"

### MCP Server Pattern

This project follows the FastMCP pattern:
- `@mcp.resource()`: Decorator for defining resources that clients can fetch
- `@mcp.tool()`: Decorator for defining tools that clients can invoke
- Resources use URI templates (e.g., `resource://pattern/{param}`)

### Current Implementation

- **Configuration**: `HARMONY_HELP_PATH` environment variable defines the path to Harmony help documentation
- **Resource `harmony://config/help-path`**: Returns the configured help path and whether it exists
- The server reads from the local Harmony help documentation folder to provide context

## Development Notes

- Resources should provide static or dynamic information about Harmony and their API
- Tools can be added to help interact with or query Harmony API documentation
- Follow FastMCP conventions for resource URI patterns and tool naming
