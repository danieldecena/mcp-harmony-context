# MILO ANIMATION PROJECT

## What this project is
A 60-second memorial short animation about Milo, a French
Bulldog. Built in Toon Boom Harmony 25.2 Premium.
Scripted via Harmony's JavaScript Script Editor.

## Stack
- Toon Boom Harmony 25.2 Premium (Mac)
- JavaScript scripts → run in Harmony Script Editor
- After Effects for compositing + aura effects
- Scripts live at:
  ~/Library/Preferences/Toon Boom Animation/
  Toon Boom Harmony Premium/2500-scripts/

## Key files
- MiloMasterRun.js  → runs all steps in order
- MiloSetup.js      → layers + color palette
- MILO_GOAL.md      → full spec, done criteria, API rules

## Scene structure
- 1440 frames @ 24fps = 60 seconds
- Scene 1 (1-360):    Sleeping / Cozy Home
- Scene 2 (361-1200): Golden Hour / Playful
- Scene 3 (1201-1440): Doggy Heaven

## Layers (bottom to top)
BG_Heaven, BG_GoldenHour, BG_CozyHome,
MILO_Leg_BR, MILO_Leg_BL, MILO_Leg_FR, MILO_Leg_FL,
MILO_Body_A, MILO_Wrinkles_B3, MILO_Mouth_B4,
MILO_Eyes_B2, MILO_Head_B1

## Colors (never change these HEX values)
Coat_Fawn #C8A876 | Cream_Belly #E8D9BC
Eyes_Brown #6B4226 | Nose_Dark #3D2314
Ear_Blush #E8B89A | Linework #2C1A0E
Shadow #A8845A | Moms_Aura #B8A0D4
Aura_Lavender #D4C0E8 | Aura_Blue #A0B8D4
Heaven_Blue #B8D4F0 | Heaven_White #E8F4FF
Sky_Gold #F5C842 | Grass_Rich #7A9E4E
Home_Warm #E8D5B0 | Lamp_Glow #FFE0A0

## Harmony API rules
### USE THESE
- scene.setStopFrame(1440)
- Timeline.addDTLayer("name", "READ")
- PaletteObjectManager.createScenePalette("name")
- node.setAsDefaultCamera(nodePath)
- node.type(nodePath)
- Drawing.create(columnName, drawingName)
- MessageLog.trace("message")

### NEVER USE (does not exist)
- DrawingTools.createLayers()
- scene.setDefaultCamera()
- scene.setMarkerComment()
- node.getNodePath()

## Done criteria
1. MiloMasterRun.js runs with zero errors
2. All 12 layers in Timeline
3. Milo_Colors palette has 16 colors
4. Console shows manual drawing instructions
5. Final message: "MILO SCENE READY"

## Character
- French Bulldog, fawn coat, NO bandana
- Bat ears, dark muzzle, soft wrinkles
- White chest patch, short nub tail
- Mom's purple/blue aura (#B8A0D4) in every scene

## Full spec
See MILO_GOAL.md for complete details.
