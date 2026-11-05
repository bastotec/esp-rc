
## Interactive web viewer (`viewer/web/`)

`index.html` + `car.glb` (all 118 parts as named meshes, built by `tools/web_glb.py` from `viewer/parts`).
Colours: orange = designed by us, grey = Tarmo5 parts reused, green = bought electronics, blue = 18650s, dark = other bought parts.
Explode slider, and Play animates the drive (wheels, motor, pinion, main gear), steering (servo horn, steering bar, front uprights) and suspension (arms pivot on their measured hinge holes; shocks follow).
The animation is illustrative: travel and speeds are not simulated, and the rear arms are swung through a small fixed angle.
Serve the folder statically (e.g. `python3 -m http.server -d viewer/web`); it loads three.js from jsdelivr.
