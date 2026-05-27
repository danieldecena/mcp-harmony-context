import os, json, subprocess, sys, shutil

HOME = os.path.expanduser("~")
DEST = f"{HOME}/Developer/sandbox/mcp-harmony-context"
CONFIG = f"{HOME}/Library/Application Support/Claude/claude_desktop_config.json"

# Clone
if not os.path.exists(DEST):
    os.makedirs(os.path.dirname(DEST), exist_ok=True)
    subprocess.run(["git","clone","https://github.com/jorgehi/mcp-harmony-context.git",DEST])

# Find harmony path
harmony_help = "/Applications/Toon Boom Harmony 25.2 Premium/Harmony 25.2 Premium.app/Contents/tba/resources/help"
for p in [harmony_help]:
    if os.path.exists(p): break

# .env
with open(f"{DEST}/.env","w") as f: f.write(f"HARMONY_HELP_PATH={harmony_help}\n")

# uv sync
uv = shutil.which("uv") or f"{HOME}/.local/bin/uv"
subprocess.run([uv,"sync"],cwd=DEST)

# Update config
with open(CONFIG) as f: cfg = json.load(f)
cfg["mcpServers"]["harmony-context"] = {"command":uv,"args":["--directory",DEST,"run","main.py"],"env":{"HARMONY_HELP_PATH":harmony_help}}
with open(CONFIG,"w") as f: json.dump(cfg,f,indent=2)

print("DONE")
