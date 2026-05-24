// MiloSetup — STEP 1
// Sets stop frame, builds the 12-layer Milo rig timeline, and creates
// the Milo_Colors palette with all 16 production colors.

function MiloSetup() {
    scene.setStopFrame(1440);

    // Wipe the default "Drawing" layer if Harmony auto-created one.
    if (node.getName("Top/Drawing") === "Drawing") {
        node.deleteNode("Top/Drawing", true, true);
    }

    var layers = [
        "BG_Heaven", "BG_GoldenHour", "BG_CozyHome",
        "MILO_Leg_BR", "MILO_Leg_BL", "MILO_Leg_FR", "MILO_Leg_FL",
        "MILO_Body_A",
        "MILO_Wrinkles_B3", "MILO_Mouth_B4", "MILO_Eyes_B2", "MILO_Head_B1"
    ];
    // node.add stacks layers vertically in the network; Timeline picks them up automatically.
    for (var i = 0; i < layers.length; i++) {
        node.add("Top", layers[i], "READ", 0, i * 50, 0);
    }

    var palette = PaletteObjectManager.getScenePaletteList(scene.currentScene())
        .createPalette("Milo_Colors", 0);

    var colors = [
        ["Coat_Fawn",     0xC8, 0xA8, 0x76],
        ["Cream_Belly",   0xE8, 0xD9, 0xBC],
        ["Eyes_Brown",    0x6B, 0x42, 0x26],
        ["Nose_Dark",     0x3D, 0x23, 0x14],
        ["Ear_Blush",     0xE8, 0xB8, 0x9A],
        ["Linework",      0x2C, 0x1A, 0x0E],
        ["Shadow",        0xA8, 0x84, 0x5A],
        ["Moms_Aura",     0xB8, 0xA0, 0xD4],
        ["Aura_Lavender", 0xD4, 0xC0, 0xE8],
        ["Aura_Blue",     0xA0, 0xB8, 0xD4],
        ["Heaven_Blue",   0xB8, 0xD4, 0xF0],
        ["Heaven_White",  0xE8, 0xF4, 0xFF],
        ["Sky_Gold",      0xF5, 0xC8, 0x42],
        ["Grass_Rich",    0x7A, 0x9E, 0x4E],
        ["Home_Warm",     0xE8, 0xD5, 0xB0],
        ["Lamp_Glow",     0xFF, 0xE0, 0xA0]
    ];
    for (var c = 0; c < colors.length; c++) {
        var col = palette.addNewColor();
        col.setName(colors[c][0]);
        col.setColorType(PaletteColor.SOLID_COLOR);
        col.setRGBA(colors[c][1], colors[c][2], colors[c][3], 255);
    }

    MessageLog.trace("MiloSetup: 12 layers + Milo_Colors palette ready.");
}
