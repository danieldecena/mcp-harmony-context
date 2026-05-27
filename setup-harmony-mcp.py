#!/usr/bin/env python3
"""
Auto-setup Harmony MCP for Milo project
Runs entirely from Python - no bash needed
"""
import os
import json
import shutil
import subprocess
import sys

print("======================================")
print("  HARMONY MCP AUTO-SETUP")
print("======================================\n")

HOME = "/Users/daniel"
DEST = f"{HOME}/Developer/sandbox/mcp-harmony-context"
CONFIG_PATH = f"{HOME}/Library/Application Support/Claude/claude_desktop_config.json"

# Step 1: Clone repo
print("→ Setting up repo...")
if os.path.exists(DEST):
    print("  Already exists - skipping clone")
else:
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    result = subprocess.run(
        ["git", "clone", "https://github.com/jorgehi/mcp-harmony-context.git", DEST],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ❌ Clone failed: {result.stderr}")
        sys.exit(1)
    print("  ✅ Repo cloned")

# Step 2: Find Harmony help path
print("\n→ Finding Harmony help docs...")
possible = [
    "/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help",
    "/Applications/Toon Boom Harmony 25 Premium/Harmony 25 Premium.app/Contents/tba/resources/help",
]
harmony_help = None
for p in possible:
    if os.path.exists(p):
        harmony_help = p
        break

if not harmony_help:
    # Search for it
    result = subprocess.run(
        ["find", "/Applications", "-name", "help", "-path", "*/tba/*"],
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        if "harmony" in line.lower() or "Harmony" in line:
            harmony_help = line.strip()
            break

if not harmony_help:
    harmony_help = "/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"
    print(f"  ⚠️  Could not auto-find, using default path")
else:
    print(f"  ✅ Found: {harmony_help}")

# Step 3: Write .env
print("\n→ Writing .env...")
env_path = os.path.join(DEST, ".env")
with open(env_path, "w") as f:
    f.write(f"HARMONY_HELP_PATH={harmony_help}\n")
print("  ✅ .env written")

# Step 4: Install deps
print("\n→ Installing dependencies...")
uv_path = shutil.which("uv") or f"{HOME}/.local/bin/uv"
result = subprocess.run(
    [uv_path, "sync"],
    cwd=DEST,
    capture_output=True, text=True
)
if result.returncode != 0:
    print(f"  ❌ uv sync failed: {result.stderr}")
    sys.exit(1)
print("  ✅ Dependencies installed")

# Step 5: Update Claude Desktop config
print("\n→ Updating Claude Desktop config...")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

config["mcpServers"]["harmony-context"] = {
    "command": uv_path,
    "args": ["--directory", DEST, "run", "main.py"],
    "env": {
        "HARMONY_HELP_PATH": harmony_help
    }
}

with open(CONFIG_PATH, "w") as f:
    json.dump(config, f, indent=2)
print("  ✅ Claude Desktop config updated")

print("\n======================================")
print("  ✅ ALL DONE!")
print("======================================")
print("\nNext steps:")
print("1. Restart Claude Desktop")
print("2. Harmony MCP will be active")
print("3. I'll have full Harmony API access")
print(f"\nRepo: {DEST}")
print(f"Help path: {harmony_help}")
