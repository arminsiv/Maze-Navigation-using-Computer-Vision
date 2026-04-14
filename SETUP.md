# Setup Guide

Follow these steps to set up the Maze Navigation project on your machine.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git
- iRobot Create3 robot
- Overhead camera setup
- Bluetooth-enabled computer

## Installation Steps

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Maze-Navigation-using-Computer-Vision
```

### 2. Create a Virtual Environment (Recommended)

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

Test that all packages are installed correctly:

```bash
python -c "import cv2, numpy, yaml; print('✓ Core packages installed')"
python -c "from irobot_edu_sdk.robots import Create3; print('✓ iRobot SDK installed')"
```

### 5. Set Up Directories

The following directories will be auto-created when scripts run:

```bash
mkdir -p data/calibration_checkerboards
mkdir -p calibration
mkdir -p output
mkdir -p logs
```

Or run the included Python scripts which will create these automatically.

## Configuration

### Customize Paths and Parameters

Edit `config.yaml` to set:

1. **Input/Output Paths** — Change directories if your data is stored elsewhere
2. **Robot Parameters** — Adjust `MOVEMENT_SCALE_CORRECTION` based on calibration
3. **Camera Calibration** — Update checkerboard parameters if using different pattern
4. **Logging** — Enable/disable verbose output

Example:
```yaml
robot:
  initial_heading: 0.0
  movement_scale_correction: 0.85  # Change this if robot overshoots
```

## Running the Project

### Step 1: Camera Calibration
```bash
jupyter notebook src/camera_calibration.ipynb
```
- Collect checkerboard images
- Generate calibration parameters
- Outputs saved to `calibration/`

### Step 2: Homography Transformation
```bash
python src/Homography.py
```
- Loads calibrated image
- Click to select maze corners
- Generates top-down perspective view

### Step 3: Pathfinding (Manual or External)
Use your A* implementation or external tool to generate:
- `data/astar_path_simplified.npy` — Array of N×2 waypoints

### Step 4: Robot Navigation
```bash
python src/robot_navi.py
```
- Ensure iRobot Create3 is powered on
- Connect via Bluetooth
- Robot will automatically navigate the maze

## Troubleshooting

### Issue: "Module not found" errors
**Solution:** Reinstall packages
```bash
pip install --upgrade -r requirements.txt
```

### Issue: Robot doesn't connect via Bluetooth
**Solution:**
1. Ensure robot is powered on
2. Check Bluetooth is enabled on your computer
3. Verify robot name in `config.yaml` matches actual robot
4. Run: `python -c "from irobot_edu_sdk.backend.bluetooth import Bluetooth; print(Bluetooth.available_robots())"`

### Issue: Camera image is distorted
**Solution:**
1. Re-run camera calibration (`camera_calibration.ipynb`)
2. Use more checkerboard images (10+ recommended)
3. Ensure checkerboard fills most of the camera frame

### Issue: Robot overshoots or undershoots distances
**Solution:** Adjust `MOVEMENT_SCALE_CORRECTION` in `config.yaml`
- Increase value (closer to 1.0) if robot undershoots
- Decrease value (closer to 0.8) if robot overshoots
- Test with small increments (±0.05)

### Issue: Waypoint file not found
**Solution:** Ensure `data/astar_path_simplified.npy` exists before running robot navigation

## File Organization

```
project/
├── src/                    # Source code
├── Final_output/           # Results
├── config.yaml             # Configuration
└── requirements.txt        # Dependencies
```

## Next Steps

1. **Calibrate Camera** — Run camera_calibration.ipynb
2. **Generate Homography** — Run Homography.py
3. **Prepare Pathfinding** — Generate waypoints using A* algorithm
4. **Test Robot Navigation** — Run robot_navi.py with path

## Support

For issues or questions:
1. Check the [README.md](README.md) for project overview
2. Review [config.yaml](config.yaml) for configuration options
3. Check logs in `logs/` directory for detailed error messages
4. Verify all prerequisites are installed

## Additional Resources

- [OpenCV Documentation](https://docs.opencv.org/)
- [iRobot Create3 SDK](https://github.com/iRobot-Education/Create3-SDK)
- [NumPy Documentation](https://numpy.org/doc/)

---

**Last Updated:** April 2026
