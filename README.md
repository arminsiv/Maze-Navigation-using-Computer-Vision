# Maze Navigation using Computer Vision

A vision-based autonomous navigation system for the iRobot Create3 robot. The robot successfully navigates a 470×417 cm maze using overhead camera feed, real-time image processing with OpenCV, and the A* pathfinding algorithm.

## 🎯 Project Overview

This project demonstrates an efficient lightweight alternative to traditional SLAM and GPS-based navigation by leveraging:
- **Computer Vision**: Overhead camera system for real-time maze perception
- **Image Processing**: OpenCV for perspective transformation and maze analysis
- **Pathfinding**: A* algorithm for optimal path generation
- **Robot Control**: iRobot Create3 with Bluetooth communication

The system achieves autonomous maze navigation without onboard sensors, making it cost-effective and scalable.

## 🏗️ System Architecture

### 1. **Camera Calibration** (`camera_calibration.ipynb`)
- Calibrates the overhead camera to correct lens distortion
- Creates a camera matrix and distortion coefficients
- Ensures accurate image processing for maze detection

### 2. **Homography Transformation** (`Homography.py`)
- Converts the camera's perspective view to a top-down 2D view
- Manual corner selection for precise calibration
- Outputs: Perspective-corrected maze image (1410×1251 pixels)

### 3. **Pathfinding** 
- Analyzes the corrected maze image
- Implements A* algorithm to find the optimal path
- Generates waypoint sequence for robot navigation

### 4. **Robot Navigation** (`robot_navi.py`)
- Executes the computed path on the iRobot Create3
- Real-time position tracking and heading control
- Adaptive movement with distance correction (0.85 scale factor)
- Communication via Bluetooth

## 🔧 Hardware Requirements

- **Robot**: iRobot Create3
- **Camera**: Overhead camera (mounted above maze for top-down view)
- **Communication**: Bluetooth-enabled computer
- **Maze**: Physical maze setup (470×417 cm reference)

## 💻 Software Requirements

- Python 3.7+
- OpenCV (`cv2`)
- NumPy
- iRobot Education SDK (`irobot_edu_sdk`)
- Jupyter Notebook

### Installation

```bash
pip install opencv-python numpy irobot-edu-sdk jupyter
```

## 🚀 Usage

### Step 1: Camera Calibration
1. Open `camera_calibration.ipynb`
2. Capture calibration images of a checkerboard pattern
3. Generate camera calibration parameters

### Step 2: Homography & Perspective Correction
1. Run `Homography.py`
2. Click the 4 corners of your maze in the camera feed:
   - Top-Left
   - Top-Right
   - Bottom-Right
   - Bottom-Left
3. Generates perspective-corrected top-down maze image

### Step 3: Maze Analysis & Pathfinding
1. Analyze the corrected maze image
2. Extract black walls and white space
3. Run A* algorithm to generate waypoints
4. Output: `astar_path_simplified.npy` (coordinate array)

### Step 4: Robot Navigation
1. Connect iRobot Create3 via Bluetooth
2. Run `robot_navi.py`
3. Robot will:
   - Load waypoints from `astar_path_simplified.npy`
   - Follow the computed path
   - Display real-time progress in console

```python
# Load and use configuration in your Python files
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# Access paths
input_path = config['paths']['input']['undistorted_image']
output_path = config['paths']['output']['maze_topdown']

# Access robot settings
initial_heading = config['robot']['initial_heading']
movement_correction = config['robot']['movement_scale_correction']
```

## 📁 Project Structure

```
Maze-Navigation-using-Computer-Vision/
├── src/                           # Source code directory
│   ├── camera_calibration.ipynb   # Camera calibration pipeline
│   ├── Homography.py              # Perspective transformation
│   ├── robot_navi.py              # Robot navigation control
│   └── Robot.ipynb                # Robot control notebook
│
│
├── Final_output/                        # Generated outputs
│   ├── maze_topdown.png           # Perspective-corrected maze image
│   ├── Astar.jpeg                 # A* pathfinding visualization
│   ├── movement.jpeg              # Robot movement trace
│   └── Test.MOV                   # Navigation video recording
│
├── config.yaml                    # Configuration file (paths, parameters)
├── README.md                      # This file
├── LICENSE                        # Project license
└── .git/                          # Version control
```

## 📋 File Guide

### Configuration
- **config.yaml** — Master configuration file defining all paths, parameters, and settings
  - Edit this file to change input/output directories
  - Update robot parameters (heading, movement correction)
  - Modify camera calibration checkerboard parameters
  - Configure logging verbosity

### Source Code Files
- **camera_calibration.ipynb** — Jupyter notebook for camera calibration
  - Input: Checkerboard pattern images
  - Output: `calibration/camera_matrix.npy`, `calibration/distortion_coeff.npy`
  - Run first to generate calibration data

- **Homography.py** — Perspective transformation script
  - Input: `data/undistorted_image_output.png`
  - Process: Manual corner selection for 4 maze corners
  - Output: `output/maze_topdown.png`, `calibration/homography_matrix.npy`
  - Requires: PyYAML (`pip install pyyaml`)

- **robot_navi.py** — Main robot navigation script
  - Input: `data/astar_path_simplified.npy` (waypoints)
  - Process: Loads waypoints and executes navigation on iRobot Create3
  - Output: Console logs with real-time position/heading updates
  - Requires: iRobot SDK, Bluetooth connection

- **Robot.ipynb** — Alternative robot control interface (notebook version)
  - For interactive robot testing and debugging
  - Allows step-by-step control and visualization

## 🔧 Configuration File (config.yaml)

The `config.yaml` file is the central hub for all project settings:

```yaml
paths:
  input:
    raw_camera_image: "./data/raw_camera_image.png"
    undistorted_image: "./data/undistorted_image_output.png"
  output:
    maze_topdown: "./output/maze_topdown.png"
  calibration:
    camera_matrix: "./calibration/camera_matrix.npy"
    homography_matrix: "./calibration/homography_matrix.npy"
  pathfinding:
    waypoints: "./data/astar_path_simplified.npy"

robot:
  initial_heading: 0.0              # degrees
  movement_scale_correction: 0.85   # 0.85 = 15% reduction
  connection_type: "bluetooth"
  robot_name: "Robot 3"

homography:
  output_width: 1410
  output_height: 1251
  maze_width_cm: 470
  maze_height_cm: 417
```

**Edit this file to:**
- Change input/output directories
- Adjust robot movement scale if it overshoots/undershoots
- Modify initial robot heading
- Update logging preferences

## 📊 Results

- **Maze Size**: 470×417 cm
- **Pathfinding**: A* algorithm finds optimal route
- **Success Rate**: Autonomous navigation completed
- **Output Files**: 
  - Top-down perspective-corrected maze image
  - A* pathfinding visualization
  - Robot movement trajectory
  - Navigation video recording

See `Final_outputs/` for detailed results.

## 🔑 Key Features

- ✅ Real-time overhead camera perception
- ✅ Automatic perspective correction
- ✅ Optimal path computation (A* algorithm)
- ✅ Bluetooth robot control
- ✅ Accurate position tracking and heading control
- ✅ Lightweight and cost-effective alternative to SLAM

## 📝 Notes

- **Movement Correction**: The robot may overshoot; adjust `MOVEMENT_SCALE_CORRECTION` in `robot_navi.py` if needed
- **Calibration**: Precise corner selection in Homography is crucial for accurate navigation
- **Lighting**: Ensure consistent lighting for camera calibration and maze detection

## 📄 License

This project is licensed under the LICENSE file in this repository.

## 👥 Contributors

This is a collaborative project developed as part of a software systems engineering course.

---

**Last Updated**: April 2026
