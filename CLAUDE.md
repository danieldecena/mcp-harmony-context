# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two things coexist here:

1. **mcp-harmony-context** (`main.py`) — an MCP server (FastMCP) that exposes
   Toon Boom Harmony's API documentation to AI assistants. Forked / authored
   by Jorge Hernandez Ibañez. Reads from a local Harmony install OR a mirrored
   help directory built via `scripts/fetch_harmony_docs.py`.
2. **The Milo animation project** (`harmony-scripts/`, `MILO_GOAL.md`) — a
   60-second memorial short for Milo (French Bulldog) built in Toon Boom
   Harmony 25.2 Premium. The MCP server above is what feeds Claude the
   Harmony API knowledge needed to write/validate these scripts.

## Setup

```bash
# Python 3.12+ required
uv sync                                    # installs deps from uv.lock
# OR: pip install -e .

# Optional: set custom help-doc path
export HARMONY_HELP_PATH=~/path/to/harmony-help

# Optional: mirror the public docs (if no local Harmony install)
uv run scripts/fetch_harmony_docs.py
```

## Run the MCP server

```bash
uv run python main.py                      # direct
./install-harmony-mcp.sh                   # registers in Claude Desktop config
python3 setup-harmony-mcp.py               # interactive setup
```

Registered in `~/Library/Application Support/Claude/claude_desktop_config.json`
under the name `harmony-context` (or similar — see `harmony-mcp-config.json`).

## MCP tools exposed

- `list_api_classes` — browse all Harmony API classes
- `get_api_class` — full docs for one class
- `search_api` — keyword search across class names + descriptions
- `list_demo_scripts` / `get_demo_script` — Harmony's bundled `.js` examples
- `harmony://config/diagnostics` resource — reports which configured paths exist

## Run tests

```bash
uv run pytest                              # all tests
uv run pytest tests/test_main.py -v        # verbose
```

`tests/conftest.py` provides fixtures from `tests/fixtures/`. The MCP server
should be testable without a real Harmony install.

## Validate Harmony API usage in scripts

When writing or editing `harmony-scripts/*.js`, validate any new API calls:
```bash
uv run scripts/validate_harmony_api.py harmony-scripts
```

## ── Milo animation project ──────────────────────────────────────────────────

This section is unique to the animation, not the MCP server.

### Scripts live in two places

- `harmony-scripts/` — source of truth in this repo (git-tracked)
- `~/Library/Preferences/Toon Boom Animation/Toon Boom Harmony Premium/2500-scripts/`
  — where Harmony's Script Editor actually loads them

Keep them in sync. `install-harmony-mcp.sh` and related scripts may sync them
for you; otherwise copy manually.

### Key script files

- `MiloMasterRun.js` — orchestrator, runs all setup steps in order
- `MiloSetup.js` — creates 12 layers + 16-color palette
- `MiloRig.js`, `MiloDrawings.js`, `MiloExpressions.js`, `MiloBackgrounds.js`,
  `MiloCamera.js`, `MiloSceneVisibility.js` — per-domain setup

### Scene structure
- 1440 frames @ 24fps = 60 seconds total
- Scene 1 (1–360): Sleeping / Cozy Home
- Scene 2 (361–1200): Golden Hour / Playful
- Scene 3 (1201–1440): Doggy Heaven

### Layers (bottom → top)
BG_Heaven, BG_GoldenHour, BG_CozyHome,
MILO_Leg_BR, MILO_Leg_BL, MILO_Leg_FR, MILO_Leg_FL,
MILO_Body_A, MILO_Wrinkles_B3, MILO_Mouth_B4,
MILO_Eyes_B2, MILO_Head_B1

### Colors — never change these HEX values
```
Coat_Fawn      #C8A876   Cream_Belly   #E8D9BC
Eyes_Brown     #6B4226   Nose_Dark     #3D2314
Ear_Blush      #E8B89A   Linework      #2C1A0E
Shadow         #A8845A   Moms_Aura     #B8A0D4
Aura_Lavender  #D4C0E8   Aura_Blue     #A0B8D4
Heaven_Blue    #B8D4F0   Heaven_White  #E8F4FF
Sky_Gold       #F5C842   Grass_Rich    #7A9E4E
Home_Warm      #E8D5B0   Lamp_Glow     #FFE0A0
```

### Character constraints
- French Bulldog, fawn coat, **NO bandana**
- Bat ears, dark muzzle, soft wrinkles
- White chest patch, short nub tail
- Mom's purple/blue aura (#B8A0D4) appears in every scene

### Harmony API — USE these
- `scene.setStopFrame(1440)`
- `node.add("Top", "name", "READ", x, y, z)` — adds Read layer; Timeline picks it up
- `PaletteObjectManager.getScenePaletteList(scene.currentScene()).createPalette("name", 0)`
- `node.setAsDefaultCamera(nodePath)`
- `node.type(nodePath)`
- `node.setTextAttr(nodePath, "ATTR", frame, value)` — **not `setAttr`**
- `Drawing.create(columnName, drawingName)`
- `MessageLog.trace("message")`

### Harmony API — NEVER use (don't exist in Harmony 25)
- `DrawingTools.createLayers()`
- `scene.setDefaultCamera()`
- `scene.setMarkerComment()`
- `node.getNodePath()`
- `Timeline.addDTLayer()` — use `node.add()` instead
- `PaletteObjectManager.createScenePalette()` — use `getScenePaletteList(...).createPalette()`
- `node.setAttr()` — use `node.setTextAttr()` with `(path, attr, frame, value)`

### Done criteria (animation)
1. `MiloMasterRun.js` runs with zero errors
2. All 12 layers present in Timeline
3. `Milo_Colors` palette has 16 colors
4. Console shows manual drawing instructions
5. Final message: `"MILO SCENE READY"`

### Full spec
See [MILO_GOAL.md](MILO_GOAL.md) for complete details, success criteria, and
extended API rules.
