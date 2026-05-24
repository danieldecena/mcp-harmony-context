// MiloSceneVisibility — STEP 6
// Drives BG visibility across the 3 act windows by toggling the layer
// enable attribute over the relevant frame ranges.

function _setEnabled(path, frameNum, enabled) {
    if (node.getName(path) === "") return;
    if (node.type(path) !== "READ") return;
    node.setTextAttr(path, "ENABLED", frameNum, enabled ? "1" : "0");
}

function MiloSceneVisibility() {
    // Scene 1 — frames 1..360 — CozyHome only
    for (var f = 1; f <= 360; f++) {
        _setEnabled("Top/BG_CozyHome",   f, true);
        _setEnabled("Top/BG_GoldenHour", f, false);
        _setEnabled("Top/BG_Heaven",     f, false);
    }
    // Scene 2 — frames 361..1200 — GoldenHour only
    for (f = 361; f <= 1200; f++) {
        _setEnabled("Top/BG_CozyHome",   f, false);
        _setEnabled("Top/BG_GoldenHour", f, true);
        _setEnabled("Top/BG_Heaven",     f, false);
    }
    // Scene 3 — frames 1201..1440 — Heaven only
    for (f = 1201; f <= 1440; f++) {
        _setEnabled("Top/BG_CozyHome",   f, false);
        _setEnabled("Top/BG_GoldenHour", f, false);
        _setEnabled("Top/BG_Heaven",     f, true);
    }
    MessageLog.trace("MiloSceneVisibility: BG visibility scheduled across 1440 frames.");
}
