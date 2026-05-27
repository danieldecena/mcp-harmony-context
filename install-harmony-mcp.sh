#!/bin/bash
set -e

echo "======================================"
echo "  HARMONY MCP SETUP FOR MILO PROJECT"
echo "======================================"
echo ""

# 1. Check uv
echo "→ Checking uv..."
if ! command -v uv &> /dev/null; then
    if [ -f "$HOME/.local/bin/uv" ]; then
        export PATH="$HOME/.local/bin:$PATH"
    else
        echo "  Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi
echo "  ✅ uv found: $(uv --version)"

# 2. Clone repo
echo ""
echo "→ Cloning mcp-harmony-context..."
DEST="/Users/daniel/Developer/sandbox/mcp-harmony-context"
if [ -d "$DEST" ]; then
    echo "  Already exists, pulling latest..."
    cd "$DEST" && git pull
else
    git clone https://github.com/jorgehi/mcp-harmony-context.git "$DEST"
fi
echo "  ✅ Repo ready at $DEST"

# 3. Find Harmony help path
echo ""
echo "→ Finding Harmony help docs..."
HARMONY_HELP=""
POSSIBLE_PATHS=(
    "/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"
    "/Applications/Toon Boom Harmony 25 Premium/Harmony 25 Premium.app/Contents/tba/resources/help"
    "/Applications/Toon Boom Harmony 25 Premium.app/Contents/tba/resources/help"
)
for P in "${POSSIBLE_PATHS[@]}"; do
    if [ -d "$P" ]; then
        HARMONY_HELP="$P"
        break
    fi
done

if [ -z "$HARMONY_HELP" ]; then
    # Try to find it
    HARMONY_HELP=$(find /Applications -name "help" -path "*/tba/*" 2>/dev/null | grep -i harmony | head -1)
fi

if [ -z "$HARMONY_HELP" ]; then
    echo "  ⚠️  Could not auto-find Harmony help path"
    echo "  Using fallback path..."
    HARMONY_HELP="/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"
else
    echo "  ✅ Found: $HARMONY_HELP"
fi

# 4. Write .env file
echo ""
echo "→ Writing .env config..."
cat > "$DEST/.env" << EOF
HARMONY_HELP_PATH=$HARMONY_HELP
EOF
echo "  ✅ .env written"

# 5. Install dependencies
echo ""
echo "→ Installing Python dependencies..."
cd "$DEST"
uv sync
echo "  ✅ Dependencies installed"

# 6. Find uv full path
UV_PATH=$(which uv || echo "$HOME/.local/bin/uv")

# 7. Done - print config
echo ""
echo "======================================"
echo "  ✅ SETUP COMPLETE"
echo "======================================"
echo ""
echo "Claude Desktop config entry:"
echo ""
echo '"harmony-context": {'
echo '  "command": "'$UV_PATH'",'
echo '  "args": ["--directory", "'$DEST'", "run", "main.py"],'
echo '  "env": {'
echo '    "HARMONY_HELP_PATH": "'$HARMONY_HELP'"'
echo '  }'
echo '}'
echo ""
echo "Config file location:"
echo "/Users/daniel/Library/Application Support/Claude/claude_desktop_config.json"
