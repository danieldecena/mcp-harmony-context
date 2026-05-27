#!/bin/bash
# HARMONY MCP SETUP SCRIPT
# Auto-written by Claude

echo "🎬 Setting up Harmony MCP for Milo..."

# 1. Check for uv
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.local/bin/env
fi

# 2. Clone the repo
cd /Users/daniel/Developer/sandbox
if [ ! -d "mcp-harmony-context" ]; then
    git clone https://github.com/jorgehi/mcp-harmony-context.git
fi
cd mcp-harmony-context

# 3. Create .env with Harmony path
cat > .env << 'EOF'
HARMONY_HELP_PATH=/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help
EOF

# 4. Install dependencies
uv sync

echo ""
echo "✅ Setup complete!"
echo ""
echo "Harmony MCP path:"
echo "$(pwd)/main.py"
