// MiloExpressions — STEP 4
// Maps 8 named expressions to (eyes, wrinkles, mouth) substitution combos
// and provides a helper to drop an expression at a given frame.

var MILO_EXPRESSIONS = {
    Happy:    { eyes: "eyes_open",   wrinkles: "wrinkles_neutral",   mouth: "mouth_smile"   },
    Sad:      { eyes: "eyes_half",   wrinkles: "wrinkles_furrowed",  mouth: "mouth_whimper" },
    Excited:  { eyes: "eyes_wide",   wrinkles: "wrinkles_raised",    mouth: "mouth_yawn"    },
    Tired:    { eyes: "eyes_half",   wrinkles: "wrinkles_neutral",   mouth: "mouth_yawn"    },
    Anxious:  { eyes: "eyes_wide",   wrinkles: "wrinkles_raised",    mouth: "mouth_whimper" },
    Thinking: { eyes: "eyes_half",   wrinkles: "wrinkles_furrowed",  mouth: "mouth_rest"    },
    Confused: { eyes: "eyes_wide",   wrinkles: "wrinkles_furrowed",  mouth: "mouth_rest"    },
    Sleeping: { eyes: "eyes_closed", wrinkles: "wrinkles_neutral",   mouth: "mouth_rest"    }
};

function _setSubstitution(layerPath, frameNum, drawingName) {
    var col = node.linkedColumn(layerPath, "DRAWING.ELEMENT");
    if (col === "") return false;
    column.setEntry(col, 1, frameNum, drawingName);
    return true;
}

function applyMiloExpression(name, frameNum) {
    var combo = MILO_EXPRESSIONS[name];
    if (!combo) {
        MessageLog.trace("applyMiloExpression: unknown '" + name + "'");
        return;
    }
    _setSubstitution("Top/MILO_Eyes_B2",     frameNum, combo.eyes);
    _setSubstitution("Top/MILO_Wrinkles_B3", frameNum, combo.wrinkles);
    _setSubstitution("Top/MILO_Mouth_B4",    frameNum, combo.mouth);
    MessageLog.trace("Frame " + frameNum + ": " + name);
}

function MiloExpressions() {
    MessageLog.trace("MiloExpressions: 8 expression combos registered.");
    for (var name in MILO_EXPRESSIONS) {
        var c = MILO_EXPRESSIONS[name];
        MessageLog.trace("  " + name + " = " + c.eyes + " + " + c.wrinkles + " + " + c.mouth);
    }
    MessageLog.trace("Use applyMiloExpression(\"Happy\", 120) to set a frame.");
}
