#!/bin/bash
# ONE-COMMAND HARMONY MCP INSTALLER
# Run this in Terminal: bash ~/Developer/sandbox/install.sh

set -e
echo "🎬 Installing Harmony MCP..."

# Setup paths
DEST="$HOME/Developer/sandbox/mcp-harmony-context"
UV="$HOME/.local/bin/uv"
CONFIG="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
HARMONY="/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"

# Clone repo
echo "→ Cloning repo..."
mkdir -p "$HOME/Developer/sandbox"
[ -d "$DEST" ] && rm -rf "$DEST"
git clone https://github.com/jorgehi/mcp-harmony-context.git "$DEST"

# Write .env
echo "HARMONY_HELP_PATH=$HARMONY" > "$DEST/.env"
echo "→ .env written"

# Install deps
echo "→ Installing dependencies..."
cd "$DEST"
$UV sync
echo "→ Dependencies installed"

# Update Claude Desktop config using Python
echo "→ Updating Claude Desktop config..."
python3 - << PYEOF
import json

config_path = "$CONFIG"
dest = "$DEST"
uv = "$UV"
harmony = "$HARMONY"

with open(config_path) as f:
    cfg = json.load(f)

cfg["mcpServers"]["harmony-context"] = {
    "command": uv,
    "args": ["--directory", dest, "run", "main.py"],
    "env": {"HARMONY_HELP_PATH": harmony}
}

with open(config_path, "w") as f:
    json.dump(cfg, f, indent=2)

print("Config updated!")
PYEOF

echo ""
echo "✅ DONE! Now:"
echo "  1. Quit Claude Desktop (CMD+Q)"
echo "  2. Reopen Claude Desktop"
echo "  3. harmony-context MCP will be active"
