# Virtual Camera 3D

> Software 3D renderer with a movable virtual camera: perspective projection, transformations, zoom and face sorting.

The scene is rendered without a 3D engine: every vertex goes through hand-written 4x4 transformation matrices (`transformations.py`), a view matrix of the camera (`camera.py`) and a perspective projection. Faces are sorted by distance to the camera (painter's algorithm) before drawing with Pygame.

## Run

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Keys | Action |
|---|---|
| Arrow keys | Move left / right / up / down |
| `W` / `S` | Move forward / backward |
| `I` / `K` | Pitch |
| `A` / `D` | Yaw |
| `Q` / `E` | Roll |
| `R` | Reset rotation |
| `Z` / `C` / `X` | Zoom in / out / reset |

---

Built as coursework for Applied Computer Science at Warsaw University of Technology.
