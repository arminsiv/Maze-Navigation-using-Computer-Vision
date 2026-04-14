import cv2
import numpy as np
import yaml
import os
from pathlib import Path

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Get paths from config
INPUT_IMAGE = config['paths']['input']['undistorted_image']
OUTPUT_IMAGE = config['paths']['output']['maze_topdown']
OUTPUT_WIDTH = config['homography']['output_width']
OUTPUT_HEIGHT = config['homography']['output_height']

# Ensure output directory exists
Path(os.path.dirname(OUTPUT_IMAGE)).mkdir(parents=True, exist_ok=True)

def click_corners(image):
    """Click 4 corners: Top-Left, Top-Right, Bottom-Right, Bottom-Left"""
    corners = []

    image_copy = image.copy()
    
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            corners.append([x, y])
            cv2.circle(image_copy, (x, y), 10, (0, 255, 0), -1)
            cv2.putText(image_copy, str(len(corners)), (x+15, y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow("Click 4 Corners", image_copy)
            print(f"Corner {len(corners)}: ({x}, {y})")
    
    # Create resizable window
    cv2.namedWindow("Click 4 Corners", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Click 4 Corners", 474, 415)  
    cv2.imshow("Click 4 Corners", image_copy)
    cv2.setMouseCallback("Click 4 Corners", mouse_callback)
    
    print("\n=== MANUAL CORNER SELECTION ===")
    print("Click the 4 CORNERS of your table in this order:")
    print("1. Top-Left corner")
    print("2. Top-Right corner")
    print("3. Bottom-Right corner")
    print("4. Bottom-Left corner")
    print("\nPress ENTER when done (need exactly 4 corners)...")
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return np.array(corners, dtype=np.float32)

# Load image
image = cv2.imread(INPUT_IMAGE)
if image is None:
    raise FileNotFoundError(f"Cannot load: {INPUT_IMAGE}")

# Get corners manually
src_points = click_corners(image)

if len(src_points) != 4:
    raise ValueError(f"Need exactly 4 corners, got {len(src_points)}")

print(f"\nSelected corners: {src_points}")

# Destination points (rectangle)
dst_points = np.array([
    [0, 0],                          # Top-Left
    [OUTPUT_WIDTH, 0],               # Top-Right
    [OUTPUT_WIDTH, OUTPUT_HEIGHT],   # Bottom-Right
    [0, OUTPUT_HEIGHT]               # Bottom-Left
], dtype=np.float32)

# Compute homography
H, _ = cv2.findHomography(src_points, dst_points)

# Warp to top-down view
top_down = cv2.warpPerspective(image, H, (OUTPUT_WIDTH, OUTPUT_HEIGHT))

# Save
cv2.imwrite(OUTPUT_IMAGE, top_down)
print(f"\n✓ Saved: {OUTPUT_IMAGE}")

# Save homography matrix
homography_path = config['paths']['calibration']['homography_matrix']
Path(os.path.dirname(homography_path)).mkdir(parents=True, exist_ok=True)
np.save(homography_path, H)
print(f"✓ Saved homography matrix: {homography_path}")
