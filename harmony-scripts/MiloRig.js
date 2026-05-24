// MiloRig — STEP 2
// Sets pivot points on every rigged Milo layer.

function _setPivot(path, x, y) {
    if (node.getName(path) === "") {
        MessageLog.trace("MiloRig: missing layer " + path);
        return;
    }
    node.setTextAttr(path, "OFFSET.X", frame.current(), String(x));
    node.setTextAttr(path, "OFFSET.Y", frame.current(), String(y));
}

function MiloRig() {
    // x, y are in Harmony fields. Adjust if your character's scale differs.
    var pivots = {
        "Top/MILO_Head_B1":     [0,  3.0],   // base of neck
        "Top/MILO_Eyes_B2":     [0,  3.6],   // eye center
        "Top/MILO_Mouth_B4":    [0,  3.2],   // mouth center
        "Top/MILO_Wrinkles_B3": [0,  3.9],   // forehead
        "Top/MILO_Body_A":      [0,  0.0],   // hip center
        "Top/MILO_Leg_FL":      [-0.6, 0.5], // hip top
        "Top/MILO_Leg_FR":      [ 0.6, 0.5],
        "Top/MILO_Leg_BL":      [-0.6, 0.2],
        "Top/MILO_Leg_BR":      [ 0.6, 0.2]
    };

    for (var path in pivots) {
        _setPivot(path, pivots[path][0], pivots[path][1]);
    }

    MessageLog.trace("MiloRig: pivots applied on " + Object.keys(pivots).length + " layers.");
    MessageLog.trace("MiloRig: add separate ear pivots + tail pivot when those sub-drawings exist.");
}
