// MiloDrawings — STEP 3 (stub: vector art must be drawn manually)
// Creates empty drawing substitution slots and logs what to draw in each.

function _createSlots(layerPath, names) {
    var col = node.linkedColumn(layerPath, "DRAWING.ELEMENT");
    if (col === "") {
        MessageLog.trace("MiloDrawings: no drawing column on " + layerPath);
        return;
    }
    for (var i = 0; i < names.length; i++) {
        Drawing.create(column.getElementIdOfDrawing(col), names[i], true, false);
    }
}

function MiloDrawings() {
    _createSlots("Top/MILO_Eyes_B2",
        ["eyes_open", "eyes_half", "eyes_closed", "eyes_wide"]);
    _createSlots("Top/MILO_Mouth_B4",
        ["mouth_rest", "mouth_sniff", "mouth_pant", "mouth_yawn",
         "mouth_whimper", "mouth_smile"]);
    _createSlots("Top/MILO_Wrinkles_B3",
        ["wrinkles_neutral", "wrinkles_raised", "wrinkles_furrowed"]);

    MessageLog.trace("===== MiloDrawings — MANUAL DRAWING REQUIRED =====");
    MessageLog.trace("Palette: Milo_Colors. Use Linework (#2C1A0E) for all outlines.");
    MessageLog.trace("MILO_Head_B1: head silhouette + bat ears, fawn coat, dark muzzle.");
    MessageLog.trace("MILO_Eyes_B2: 4 substitutions — open, half, closed, wide.");
    MessageLog.trace("MILO_Mouth_B4: 6 substitutions — rest, sniff, pant, yawn, whimper, smile.");
    MessageLog.trace("MILO_Wrinkles_B3: 3 substitutions — neutral, raised, furrowed.");
    MessageLog.trace("MILO_Body_A: chest+belly cream patch, fawn body, tail.");
    MessageLog.trace("MILO_Leg_*: each leg on its own layer, fawn with shadow underside.");
    MessageLog.trace("==================================================");
}
