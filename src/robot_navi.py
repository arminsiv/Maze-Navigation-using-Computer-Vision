import numpy as np
import math
import yaml
import os
from pathlib import Path
from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3
from irobot_edu_sdk.music import Note

# ================================================================
# CONFIGURATION
# ================================================================
# Load configuration from YAML
# Note: config.yaml is in the parent directory (project root)
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Get configuration values
INITIAL_HEADING = config['robot']['initial_heading']
MOVEMENT_SCALE_CORRECTION = config['robot']['movement_scale_correction']
WAYPOINTS_FILE = config['paths']['pathfinding']['waypoints']
ROBOT_NAME = config['robot']['robot_name']

# ================================================================
# GLOBAL STATE
# ================================================================
waypoints = None
current_waypoint_index = 0
current_position = [0.0, 0.0]
current_heading = INITIAL_HEADING

# ================================================================
# HELPER FUNCTIONS
# ================================================================
def get_angle_to_target(current, target):
    """Calculate angle from current to target"""
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    return math.degrees(math.atan2(dy, dx))

def normalize_angle(angle):
    """Normalize angle to [-180, 180]"""
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def get_distance(current, target):
    """Calculate distance between two points"""
    dx = target[0] - current[0]
    dy = target[1] - current[1]
    return math.sqrt(dx*dx + dy*dy)

# ================================================================
# NAVIGATION
# ================================================================
robot = Create3(Bluetooth(ROBOT_NAME))

@event(robot.when_play)
async def navigate(robot):
    global waypoints, current_waypoint_index, current_position, current_heading
    
    # Load waypoints
    if not os.path.exists(WAYPOINTS_FILE):
        raise FileNotFoundError(f"Waypoints file not found: {WAYPOINTS_FILE}")
    waypoints = np.load(WAYPOINTS_FILE)
    print(f"📍 Loaded {len(waypoints)} waypoints")
    print(f"   Start: {waypoints[0]}")
    print(f"   Goal:  {waypoints[-1]}")
    print(f"   Movement scale: {MOVEMENT_SCALE_CORRECTION}\n")
    
    # Initialize
    await robot.reset_navigation()
    current_position = [waypoints[0][0], waypoints[0][1]]
    current_heading = INITIAL_HEADING
    current_waypoint_index = 0
    
    print(f"🤖 Starting: ({current_position[0]:.1f}, {current_position[1]:.1f}), Heading: {current_heading:.1f}°\n")
    
    # Navigate through waypoints
    while current_waypoint_index < len(waypoints) - 1:
        current = waypoints[current_waypoint_index]
        target = waypoints[current_waypoint_index + 1]
        
        # Calculate turn needed
        target_angle = get_angle_to_target(current, target)
        turn_needed = normalize_angle(target_angle - current_heading)
        
        print(f"📐 [{current_waypoint_index}] → [{current_waypoint_index + 1}]")
        print(f"   Turn: {turn_needed:.1f}°")
        
        # Turn if needed
        if abs(turn_needed) > 3.0:
            if turn_needed > 0:
                await robot.turn_left(abs(turn_needed))
            else:
                await robot.turn_right(abs(turn_needed))
            current_heading = normalize_angle(current_heading + turn_needed)
            print(f"   ✓ New heading: {current_heading:.1f}°")
        
        # Calculate distance
        distance = get_distance(current, target)
        corrected_distance = distance * MOVEMENT_SCALE_CORRECTION
        
        print(f"   Move: {distance:.1f} cm → Corrected: {corrected_distance:.1f} cm")
        
        # Move forward with corrected distance
        await robot.set_lights_rgb(0, 0, 255)
        await robot.move(corrected_distance)
        
        # Update position (reset to target to minimize drift)
        current_position = [target[0], target[1]]
        print(f"   ✓ At: ({current_position[0]:.1f}, {current_position[1]:.1f})\n")
        
        # Next waypoint
        await robot.set_lights_rgb(0, 255, 0)
        await robot.wait(0.3)
        current_waypoint_index += 1
    
    # Completed
    print("🎉 ========================================")
    print("🎉 NAVIGATION COMPLETED!")
    print(f"🎉 Final position: ({current_position[0]:.1f}, {current_position[1]:.1f})")
    print("🎉 ========================================\n")
    
    await robot.set_lights_rgb(0, 255, 0)
    await robot.play_note(Note.C5, 0.3)
    await robot.play_note(Note.E5, 0.3)
    await robot.play_note(Note.G5, 0.5)

robot.play()
