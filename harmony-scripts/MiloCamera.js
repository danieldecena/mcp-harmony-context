// MiloCamera — STEP 5
// Creates the production camera and registers it as the scene default.

function MiloCamera() {
    var camPath = "Top/Camera_Milo";
    if (node.getName(camPath) === "") {
        camPath = node.add("Top", "Camera_Milo", "CAMERA", 0, 0, 0);
    }
    node.setAsDefaultCamera(camPath);
    MessageLog.trace("MiloCamera: default camera = " + camPath);
}
