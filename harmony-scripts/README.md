# Milo Harmony Scripts

JavaScript scripts that build the Milo scene scaffold (layers, palette,
pivots, expression combos, camera, scene visibility) in Toon Boom Harmony
25.2 Premium per `../MILO_GOAL.md`.

## Install

Copy every `Milo*.js` file into the Harmony scripts dir:

- macOS: `~/Library/Preferences/Toon Boom Animation/Toon Boom Harmony Premium/2500-scripts/`
- Windows: `%APPDATA%\Toon Boom Animation\Toon Boom Harmony Premium\2500-scripts\`

## Run

Open the Milo scene in Harmony, then in the Script Editor:

```js
MiloMasterRun();
```

Each step logs `[OK]` or `[FAIL]` and the run finishes with
`MILO SCENE READY` (or a count of failures + `MessageBox` summary).

## What is automated

- STEP 1 `MiloSetup` — stop frame, 12 layers, 16-color palette
- STEP 2 `MiloRig` — pivot offsets per layer
- STEP 3 `MiloDrawings` — drawing substitution slots + manual instructions
- STEP 4 `MiloExpressions` — 8 expression combos + `applyMiloExpression(name, frame)` helper
- STEP 5 `MiloCamera` — production camera + `node.setAsDefaultCamera`
- STEP 6 `MiloSceneVisibility` — BG enable/disable across the 3 acts
- STEP 7 `MiloBackgrounds` — manual paint instructions per scene

## What is manual

Vector art and watercolor BGs cannot be created by script. STEP 3 and
STEP 7 log the per-layer / per-scene instructions to the Script Console —
draw and paint to match.
