# MILO ANIMATION PROJECT — CLAUDE CODE GOAL

## OBJECTIVE
Complete the full Toon Boom Harmony 25.2 scene setup for 
Milo, a 60-second memorial short animation. Every script 
must run successfully from Harmony's Script Editor with 
zero errors.

---

## THE FILM
- **Character:** Milo — French Bulldog, fawn coat, no bandana
- **Runtime:** 60 seconds @ 24fps = 1440 frames
- **Resolution:** 1920x1080
- **Style:** Watercolor loose backgrounds, puppet-rigged character
- **Arc:** Sleeping (home) → Playing (golden hour) → Heaven
- **Mom's aura:** Purple/blue (#B8A0D4) present in all 3 scenes

---

## SCRIPT FILE LOCATION
```
~/Library/Preferences/Toon Boom Animation/
Toon Boom Harmony Premium/2500-scripts/MiloMasterRun.js
```

---

## WHAT MUST WORK — STEP BY STEP

### STEP 1 — MiloSetup ✅ (verify)
- Sets stop frame to 1440
- Deletes default "Drawing" layer
- Creates exactly these 12 layers in order:
  - BG_Heaven, BG_GoldenHour, BG_CozyHome
  - MILO_Leg_BR, MILO_Leg_BL, MILO_Leg_FR, MILO_Leg_FL
  - MILO_Body_A
  - MILO_Wrinkles_B3, MILO_Mouth_B4, MILO_Eyes_B2, MILO_Head_B1
- Creates "Milo_Colors" palette with exactly 16 colors:
  Coat_Fawn #C8A876, Cream_Belly #E8D9BC, Eyes_Brown #6B4226,
  Nose_Dark #3D2314, Ear_Blush #E8B89A, Linework #2C1A0E,
  Shadow #A8845A, Moms_Aura #B8A0D4, Aura_Lavender #D4C0E8,
  Aura_Blue #A0B8D4, Heaven_Blue #B8D4F0, Heaven_White #E8F4FF,
  Sky_Gold #F5C842, Grass_Rich #7A9E4E, Home_Warm #E8D5B0,
  Lamp_Glow #FFE0A0

### STEP 2 — MiloRig ✅ (verify + fix if needed)
- Sets pivot points on every layer:
  - MILO_Head_B1 → pivot at base of neck
  - MILO_Eyes_B2 → pivot at eye center
  - MILO_Mouth_B4 → pivot at mouth center
  - MILO_Wrinkles_B3 → pivot at forehead center
  - MILO_Body_A → pivot at hip center
  - MILO_Leg_FL/FR → pivot at hip top
  - MILO_Leg_BL/BR → pivot at hip top
- Ears get separate pivot at base of each ear
- Tail pivot at tail base

### STEP 3 — MiloDrawings (stub is OK)
- Cannot procedurally draw vector art in Harmony via script
- Stub must log clear instructions to the Script Console:
  - What to draw in each layer
  - Which palette colors to use
  - Which drawing substitutions to create for:
    - MILO_Eyes_B2: eyes_open, eyes_half, eyes_closed, eyes_wide
    - MILO_Mouth_B4: mouth_rest, mouth_sniff, mouth_pant, 
                     mouth_yawn, mouth_whimper, mouth_smile
    - MILO_Wrinkles_B3: wrinkles_neutral, wrinkles_raised, 
                        wrinkles_furrowed

### STEP 4 — MiloExpressions ✅ (verify + fix if needed)
- Maps 8 expressions to drawing substitution combos:
  - Happy:    eyes_open + wrinkles_neutral + mouth_smile
  - Sad:      eyes_half + wrinkles_furrowed + mouth_whimper
  - Excited:  eyes_wide + wrinkles_raised + mouth_yawn
  - Tired:    eyes_half + wrinkles_neutral + mouth_yawn
  - Anxious:  eyes_wide + wrinkles_raised + mouth_whimper
  - Thinking: eyes_half + wrinkles_furrowed + mouth_rest
  - Confused: eyes_wide + wrinkles_furrowed + mouth_rest
  - Sleeping: eyes_closed + wrinkles_neutral + mouth_rest

### STEP 5 — MiloCamera ✅ (verify + fix if needed)
- Correct API: node.setAsDefaultCamera(camPath)
- NOT: scene.setDefaultCamera()
- Remove any scene.setMarkerComment() calls

### STEP 6 — MiloSceneVisibility ✅ (verify + fix if needed)
- Use node.type() checks instead of node.getNodePath()
- Scene 1 (frames 1-360): BG_CozyHome visible only
- Scene 2 (frames 361-1200): BG_GoldenHour visible only
- Scene 3 (frames 1201-1440): BG_Heaven visible only

### STEP 7 — MiloBackgrounds (stub is OK)
- Watercolor backgrounds must be painted manually
- Stub must log per-scene color instructions:
  - Scene 1 Home: #E8D5B0 ceiling, #D4B896 wall, #C4956A floor,
                  #FFE0A0 lamp glow, #B8A0D4 aura (corner, 20%)
  - Scene 2 Golden Hour: #F5C842 sky, #B8A0D4 sky mix (30-40%),
                         #7A9E4E grass, #FFD070 sun glow
  - Scene 3 Heaven: #B8D4F0 wash, #E8F4FF mist, #FFFFFF bloom,
                    #B8A0D4 mom's aura full

### STEP 8 — MiloMasterRun (the main runner)
- Calls all steps in order with try/catch around each
- Logs SUCCESS or FAILURE per step to Script Console
- Final message: "MILO SCENE READY — Begin drawing in layers"

---

## API RULES — HARMONY 25.2

### VERIFIED WORKING
```javascript
scene.setStopFrame(1440)
Timeline.addDTLayer("name", "READ")
PaletteObjectManager.createScenePalette("name")
palette.addNewColor()
col.setName(), col.setRGBA(), col.setColorType()
PaletteColor.SOLID_COLOR
node.setAsDefaultCamera(nodePath)
node.type(nodePath)
node.coordX(), node.coordY()
Drawing.create(columnName, drawingName)
MessageLog.trace("message")
MessageBox.information("message")
```

### DO NOT USE (does not exist)
```javascript
DrawingTools.createLayers()   // no shape creation via script
scene.setDefaultCamera()      // wrong — use node.setAsDefaultCamera
scene.setMarkerComment()      // does not exist
node.getNodePath()            // does not exist
```

### DRAWING SUBSTITUTIONS
```javascript
// Correct way to create drawing substitutions:
var col = node.linkedColumn("MILO_Eyes_B2")
Drawing.create(col, "eyes_open")
Drawing.create(col, "eyes_closed")
// etc.
```

---

## DONE CRITERIA

The goal is complete when:

1. MiloMasterRun.js runs in Harmony's Script Editor 
   with zero errors
2. All 12 layers appear in the Timeline
3. Milo_Colors palette has all 16 colors
4. Script Console shows clear manual drawing instructions
5. Final message: "MILO SCENE READY"

---

## COLOR LINE REFERENCE (never change these)
| Color | Hex | Used for |
|-------|-----|----------|
| Coat_Fawn | #C8A876 | Milo's body |
| Cream_Belly | #E8D9BC | Chest patch |
| Eyes_Brown | #6B4226 | Eyes |
| Nose_Dark | #3D2314 | Nose |
| Ear_Blush | #E8B89A | Inner ear |
| Linework | #2C1A0E | All outlines |
| Shadow | #A8845A | Underside shadow |
| Moms_Aura | #B8A0D4 | Mom's presence |
| Aura_Lavender | #D4C0E8 | Aura glow |
| Aura_Blue | #A0B8D4 | Aura edge |
| Heaven_Blue | #B8D4F0 | Heaven BG |
| Heaven_White | #E8F4FF | Heaven mist |
| Sky_Gold | #F5C842 | Golden hour sky |
| Grass_Rich | #7A9E4E | Grass bottom |
| Home_Warm | #E8D5B0 | Home ceiling |
| Lamp_Glow | #FFE0A0 | Lamp light |
