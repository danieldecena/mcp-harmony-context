// MiloMasterRun — runs every Milo setup step in order with isolated
// error handling, so a failure in one step never aborts the rest.
//
// Install: copy every Milo*.js in this folder into
//   ~/Library/Preferences/Toon Boom Animation/Toon Boom Harmony Premium/2500-scripts/
//   (or the Windows equivalent), then run MiloMasterRun() from the Script Editor.

include("MiloSetup.js");
include("MiloRig.js");
include("MiloDrawings.js");
include("MiloExpressions.js");
include("MiloCamera.js");
include("MiloSceneVisibility.js");
include("MiloBackgrounds.js");

function _runStep(label, fn) {
    try {
        fn();
        MessageLog.trace("[OK]   " + label);
        return true;
    } catch (e) {
        MessageLog.trace("[FAIL] " + label + " — " + e);
        return false;
    }
}

function MiloMasterRun() {
    MessageLog.trace("===== MILO MASTER RUN =====");
    var ok = 0, fail = 0;
    var steps = [
        ["MiloSetup",           MiloSetup],
        ["MiloRig",             MiloRig],
        ["MiloDrawings",        MiloDrawings],
        ["MiloExpressions",     MiloExpressions],
        ["MiloCamera",          MiloCamera],
        ["MiloSceneVisibility", MiloSceneVisibility],
        ["MiloBackgrounds",     MiloBackgrounds]
    ];
    for (var i = 0; i < steps.length; i++) {
        if (_runStep(steps[i][0], steps[i][1])) ok++; else fail++;
    }
    MessageLog.trace("===========================");
    MessageLog.trace("OK: " + ok + "   FAIL: " + fail);
    if (fail === 0) {
        MessageLog.trace("MILO SCENE READY — Begin drawing in layers");
        MessageBox.information("MILO SCENE READY — Begin drawing in layers");
    } else {
        MessageBox.information("MILO setup completed with " + fail + " failure(s). See Script Console.");
    }
}
